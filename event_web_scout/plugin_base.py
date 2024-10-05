from .models import Event
from typing import Any


class PluginBaseMeta(type):
    def __init__(cls, name: str, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != 'PluginBase':
            if not hasattr(cls, 'name'):
                raise ValueError(f'Subclass of PluginBase must have a "name" attribute: {name}')


class PluginBase(metaclass=PluginBaseMeta):
    def __init__(self, config: dict):
        self.config = config

    def run(self) -> Any:
        raise NotImplementedError('Plugins must implement the "run(self) -> Any" method')

    def get_events(self, data: Any) -> list[Event]:
        raise NotImplementedError('Plugins must implement the "get_events(self, data: Any) -> list[Event]" method')


class LoadedPlugin:
    def __init__(self, priority: int, name: str, config: dict, _class: type[PluginBase]):
        self.priority = priority
        self.name = name
        self.config = config
        self._class = _class

    def new_instance(self) -> PluginBase:
        return self._class(self.config)
