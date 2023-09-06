class PluginInterfaceMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != 'PluginInterface':
            if not hasattr(cls, 'name'):
                raise ValueError(f'Subclass of PluginInterface must have a "name" attribute: {name}')

class PluginInterface(metaclass=PluginInterfaceMeta):
    def run(self):
        raise NotImplementedError('Subclasses must implement this method')
