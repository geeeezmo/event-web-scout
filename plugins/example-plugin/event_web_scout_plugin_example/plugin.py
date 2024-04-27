from event_web_scout.plugin_base import PluginBase
import logging
import time


class ExamplePlugin(PluginBase):
    name: str = 'ExamplePlugin'

    def __init__(self, config: dict):
        super().__init__(config)

    def run(self):
        logging.info(f'Running {self.name} with config: {self.config}')
        logging.info(f'sleeping for {self.config.get("sleep_time")} seconds')
        time.sleep(self.config.get('sleep_time'))
