from .plugin_interface import PluginInterface

class LoggingConfig():
    def __init__(self, log_dir: str, log_file_base_name: str = None, level: str = None, quiet: bool = None, format: str = None):
        self.log_dir = log_dir
        self.log_file_base_name = log_file_base_name
        self.level = level
        self.quiet = quiet
        self.format = format

class LoadedPlugin():
    def __init__(self, priority: int, name: str, config: dict, _class: PluginInterface):
        self.priority = priority
        self.name = name
        self.config = config
        self._class = _class

    def new_instance(self) -> PluginInterface:
        return self._class(self.config)