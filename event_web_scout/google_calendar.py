from datetime import datetime
from enum import Enum
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from models import DateRange
from typeguard import typechecked
from typing import Callable
import hashlib
import json
import logging
import os
import pytz
import utils

SCOPES = [
    'https://www.googleapis.com/auth/calendar'
]

EVENT_PRIVATE_PROPERTIES = {
    'plugin_name': 'event-web-scout.plugin.name',
    'event_id': 'event-web-scout.event.id',
    'event_summary': 'event-web-scout.event.summary',
    'event_start': 'event-web-scout.event.start',
    'event_end': 'event-web-scout.event.end'
}

class EventType(Enum):
    CITY =    1
    SPORTS =  2
    CULTURE = 3

EVENT_TYPE_COLORS = {
    EventType.CITY:    9,  # 5484ed
    EventType.SPORTS:  10, # 51b749
    EventType.CULTURE: 3   # dbadff
}

# EVENT_TYPE_PREFIXES = {
#     EventType.CITY:    'KAUPUNKI',
#     EventType.SPORTS:  'URHEILU',
#     EventType.CULTURE: 'KULTTUURI'
# }

DAYS_OF_WEEK = {
    'mon': 1,
    'tue': 2,
    'wed': 3,
    'thu': 4,
    'fri': 5,
    'sat': 6,
    'sun': 7
}

TIMEZONE = 'Europe/Helsinki'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


@typechecked
def to_utc_date(date: datetime) -> datetime:
    return date.replace(tzinfo=pytz.UTC)


@typechecked
def to_google_date(date: datetime, date_to_iso: Callable[[datetime], datetime] = to_utc_date) -> object:
    return {
        'dateTime': date_to_iso(date).strftime(DATETIME_FORMAT),
        'timeZone': TIMEZONE,
    }


class GoogleEventDateTime:
    def __init__(self, date_time: datetime, time_zone: str):
        self.date_time = date_time
        self.time_zone = time_zone


class GoogleEventSource:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title


# class GoogleEventStartEnd:
#     def __init__(self, start: GoogleEventDateTime, end: GoogleEventDateTime):
#         self.start = start
#         self.end = end


class GoogleEventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GoogleEvent):
            # use SHA1 hash value from event title + the start/end dates as ID
            event_sha1 = (hashlib
                         .sha1(f'{obj.summary} / {obj.start.date_time} - {obj.end.date_time}'.encode())
                         .hexdigest())

            if obj.extended_properties is None:
                extended_properties = {
                    'private': {
                        'event_sha1': event_sha1
                    }
                }
            else:
                private_extended_properties = obj.extended_properties['private']
                private_extended_properties['event_sha1'] = event_sha1
                extended_properties = obj.extended_properties | {
                    'private': private_extended_properties
                }

            return {
                'summary': obj.summary,
                'description': obj.description,
                'source': {
                    'url': obj.source.url,
                    'title': obj.source.title
                },
                'start': to_google_date(obj.start.date_time),
                'end': to_google_date(obj.end.date_time),
                'recurrence': obj.recurrence,
                'colorId': obj.color_id,
                'extendedProperties': extended_properties
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)


class GoogleEvent:
    def __init__(
            self,
            summary: str,
            description: str,
            source: GoogleEventSource,
            start: GoogleEventDateTime,
            end: GoogleEventDateTime,
            recurrence: list[str] = None,
            color_id: int = None,
            extended_properties: object = None):

        self.summary = summary
        self.description = description
        self.source = source
        self.start = start
        self.end = end
        if recurrence is None:
            self.recurrence = []
        else:
            self.recurrence = recurrence

        self.color_id = color_id
        self.extended_properties = extended_properties

    def to_json(self):
        return json.dumps(self.__dict__, cls=GoogleEventEncoder)


class GoogleCalendarUtil:
    def __init__(self, plugin_dir: str, service_account_token_file: str):
        service_account_info = json.load(open(os.path.join(plugin_dir, service_account_token_file)))
        creds = Credentials.from_service_account_info(service_account_info, scopes = SCOPES)
        self.service = build('calendar', 'v3', credentials = creds)

    @typechecked
    def check_event_exists(self, calendar_id: str, event: object) -> bool:
        private_props = event['extendedProperties']['private']
        events = self.service.events().list(
            calendarId = calendar_id,
            privateExtendedProperty = [f'{k}={v}' for k, v in private_props.items()],
            maxResults = 10,
            singleEvents = True,
            orderBy = 'startTime'
        ).execute().get('items', [])

        logging.debug('result of checking existence of event with private extended properties %s:\n%s' % (private_props, events))
        
        return len(events) > 0

    @typechecked
    def add_event(
            self,
            calendar_id: str,
            event: object,
            event_title_prefix: str = None,
            event_color: int = None):

        try:
            if self.check_event_exists(calendar_id, event):
                logging.info('Not creating event because it already exists')
            else:
                # add event type prefix to the summary
                # summary_prefix = EVENT_TYPE_PREFIXES.get(event_type)
                if event_title_prefix is not None:
                    event['summary'] = f"{event_title_prefix} {event['summary']}"
                
                # add header and footer to the event description
                event_description = ''
                if event.get('source') != None and event['source'].get('url') != None and event['source'].get('title') != None:
                    event_description += 'Tapahtuman sivu: <a href="%s" target="_blank">%s</a>' % (event['source']['url'], event['source']['title'])
                if event.get('description') != None:
                    event_description += '<hr/>%s' % event['description']
                event_description += '<hr/><i>Tämä tapahtuma luotiin automaattisesti.'
                event_description += '<br/>Jos huomaat virheen/epäjohdonmukaisuuden jossakin tämän kalenterin tapahtumissa, lähetä sähköpostia kirjoittajalle '
                event_description += 'tai luo ongelma GitHubissa'
                event_description += '<br/>This event was created automatically.'
                event_description += '<br/>If you notice an error/inconsistency in any of the events in this calendar, please email the author '
                event_description += 'or create an issue on GitHub'
                event_description += '<br/>email:  <a href="mailto:joensuutapahtumatkalenteri@gmail.com">joensuutapahtumatkalenteri@gmail.com</a>'
                event_description += '<br/>GitHub: <a href="https://github.com/geeeezmo/event-web-scout/issues">event-web-scout</a></i>'

                event['description'] = event_description

                # event_color = EVENT_TYPE_COLORS.get(event_type)
                if event_color is not None:
                    event['colorId'] = event_color
                
                # Call the Calendar API
                created_event = self.service.events().insert(calendarId = calendar_id, body = event).execute()
                logging.info(f'Event created. Link: {created_event.get("htmlLink")}')

        except HttpError as error:
            logging.error(f'An error occurred: {error}', exc_info = True)

    @typechecked
    def delete_event(self, calendar_id: str, event_id: str):
        try:
            logging.info(f'deleting event with ID {event_id}')
            self.service.events().delete(calendarId = calendar_id, eventId = event_id).execute()

        except HttpError as error:
            logging.error(f'An error occurred: {error}', exc_info = True)

    @typechecked
    def get_calendar_events(self, calendar_id: str, date_range: DateRange) -> list[any]:
        events = []

        try:
            time_min = None
            time_max = None
            if date_range.start != None:
                time_min = date_range.start.strftime(utils.DATETIME_FORMAT)
            if date_range.end != None:
                time_max = date_range.end.strftime(utils.DATETIME_FORMAT)
            events = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max
            ).execute()['items']

        except HttpError as error:
            logging.error(f'An error occurred: {error}', exc_info = True)

        return events