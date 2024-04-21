from event_web_scout.plugin_interface import PluginInterface
import logging
import time


class Plugin(PluginInterface):
    name: str = 'ExamplePlugin'

    def __init__(self, config: dict):
        super().__init__(config)

    def run(self):
        logging.info(f'Running {self.name} with config: {self.config}')
        logging.info(f'sleeping for {self.config.get("sleep_time")} seconds')
        time.sleep(self.config.get('sleep_time'))
