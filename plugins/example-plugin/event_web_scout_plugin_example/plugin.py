from event_web_scout.plugin_interface import PluginInterface
from typeguard import typechecked

class Plugin(PluginInterface):
    name: str = 'ExamplePlugin'
    
    @typechecked
    def __init__(self, config: object):
        super().__init__(config)
    
    @typechecked
    def run(self):
        print(f'Running {self.name} with config: {self.config}')
