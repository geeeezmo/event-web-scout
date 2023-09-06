from event_web_scout.plugin_interface import PluginInterface

class Plugin(PluginInterface):
    name = 'ExamplePlugin'
    
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        print(f'Running {self.name}')
