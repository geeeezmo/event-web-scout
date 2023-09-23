from event_web_scout.plugin_interface import PluginInterface
from typeguard import typechecked
import logging
import time

class Plugin(PluginInterface):
    name: str = 'ExamplePlugin'
    
    @typechecked
    def __init__(self, config: object):
        super().__init__(config)
    
    @typechecked
    def run(self):
        logging.info(f'Running {self.name} with config: {self.config}')
        # print(f'Running {self.name} with config: {self.config}')
        logging.info('sleeping for 1.8 seconds')
        time.sleep(1.8)
