from .plugin_base import PluginBase


class LoggingConfig:
    def __init__(self, log_dir: str, log_file_base_name: str = None, log_level: str = None, quiet: bool = None,
                 log_format: str = None):
        self.log_dir = log_dir
        self.log_file_base_name = log_file_base_name
        self.log_level = log_level
        self.quiet = quiet
        self.log_format = log_format


class LoadedPlugin:
    def __init__(self, priority: int, name: str, config: dict, _class: PluginBase):
        self.priority = priority
        self.name = name
        self.config = config
        self._class = _class

    def new_instance(self) -> PluginBase:
        return self._class(self.config)
