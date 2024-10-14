from datetime import datetime
from typing import Type
import json

from .datetime_utils import to_utc_date


class LoggingConfig:
    def __init__(self, log_dir: str, log_file_base_name: str = None, log_level: str = None, quiet: bool = None,
                 log_format: str = None):
        self.log_dir = log_dir
        self.log_file_base_name = log_file_base_name
        self.log_level = log_level
        self.quiet = quiet
        self.log_format = log_format


class EventSource:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title


class Event:
    def __init__(
            self,
            summary: str,
            description: str,
            start_date: datetime,
            end_date: datetime,
            time_zone: str,
            source: EventSource = None,
            extra_props: dict = None):
        self.summary = summary
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.time_zone = time_zone
        self.source = source
        self.extra_props = extra_props
        if self.extra_props is None:
            self.extra_props = {}

    def to_json(self, encoder_cls: Type[json.JSONEncoder] = None):
        if encoder_cls is not None and not issubclass(encoder_cls, json.JSONEncoder):
            raise TypeError(f"encoder_cls must be a subclass of JSONEncoder, got {encoder_cls}")

        return json.dumps(self, cls=encoder_cls)


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        datetime_format = '%Y-%m-%d %H:%M:%S %Z'
        if isinstance(obj, Event):
            return {
                'summary': obj.summary,
                'description': obj.description,
                'start': to_utc_date(obj.start_date).strftime(datetime_format),
                'end': to_utc_date(obj.end_date).strftime(datetime_format),
                'source': {
                    'url': obj.source.url,
                    'title': obj.source.title
                }
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)
