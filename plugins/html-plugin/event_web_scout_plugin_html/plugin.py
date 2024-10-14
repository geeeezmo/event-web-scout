import logging
from datetime import datetime
from typing import Any

import requests
from bs4 import BeautifulSoup
from typeguard import typechecked

from event_web_scout.models import Event, EventSource
from event_web_scout.plugin_base import PluginBase


class HtmlPlugin(PluginBase):
    name: str = 'HtmlPlugin'

    def __init__(self, config: dict):
        super().__init__(config)
        self.config = config
        if config.get('base_url') is None:
            raise RuntimeError('"base_url" config key has to be defined for HtmlPlugin')

    def run(self) -> Any:
        html_document = self.get_html_document(self.config.get('base_url'), self.config.get('url_params'))
        if html_document is None:
            return []
        else:
            # print(f'html_document.text: {html_document.text}')
            logging.info(f'html_document.text: {html_document.text}')
            return self.get_events(html_document)

    @typechecked
    def get_html_document(self, base_url: str, url_params: object = None) -> BeautifulSoup | None:
        if url_params is None:
            url_params = {}
        response = requests.get(base_url, url_params)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            logging.error('Failed to retrieve HTML document. ' +
                          f'Status code: {response.status_code}, body: ${response.content}')
            return None

    def get_events(self, data: Any) -> list[Event]:
        return []


class ExampleHtmlPlugin(HtmlPlugin):
    def get_events(self, data: Any) -> list[Event]:
        events: list[Event] = []
        if isinstance(data, BeautifulSoup):
            doc_title = data.find("head").find("title").text
            doc_description = data.select_one("body > pre").text
            start_date = data.select_one("body > p#start_date").text
            end_date = data.select_one("body > p#end_date").text
            event = Event(doc_title,
                          doc_description,
                          datetime.fromisoformat(start_date),
                          datetime.fromisoformat(end_date),
                          time_zone='UTC',
                          source=EventSource("/basic.html", "basic.html"))
            events.append(event)
        else:
            logging.error('data was not of type BeautifulSoup', data)

        return events
