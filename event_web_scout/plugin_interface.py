from typeguard import typechecked

class PluginInterfaceMeta(type):
    def __init__(cls, name: str, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != 'PluginInterface':
            if not hasattr(cls, 'name'):
                raise ValueError(f'Subclass of PluginInterface must have a "name" attribute: {name}')

class PluginInterface(metaclass=PluginInterfaceMeta):
    @typechecked
    def __init__(self, config: object = None):
        self.config = config

    @typechecked
    def run(self):
        raise NotImplementedError('Plugins must implement the "run" method')
