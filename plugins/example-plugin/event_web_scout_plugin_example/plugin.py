from typing import Any

from event_web_scout.models import Event
from event_web_scout.plugin_base import PluginBase
import logging
import time


class ExamplePlugin(PluginBase):
    name: str = 'ExamplePlugin'

    def __init__(self, config: dict):
        super().__init__(config)

    def run(self) -> Any:
        logging.info(f'Running {self.name} with config: {self.config}')
        sleep_time = self.config.get("sleep_time")
        # optionally sleep, to simulate real work
        if sleep_time:
            logging.info(f'sleeping for {sleep_time} seconds')
            time.sleep(sleep_time)
        return self.get_events(None)

    def get_events(self, data: Any) -> list[Event]:
        return list()
