class PluginBaseMeta(type):
    def __init__(cls, name: str, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != 'PluginBase':
            if not hasattr(cls, 'name'):
                raise ValueError(f'Subclass of PluginBase must have a "name" attribute: {name}')


class PluginBase(metaclass=PluginBaseMeta):
    def __init__(self, config: dict):
        self.config = config

    def run(self):
        raise NotImplementedError('Plugins must implement the "run" method')
