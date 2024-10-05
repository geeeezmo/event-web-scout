import json


class LoggingConfig:
    def __init__(self, log_dir: str, log_file_base_name: str = None, log_level: str = None, quiet: bool = None,
                 log_format: str = None):
        self.log_dir = log_dir
        self.log_file_base_name = log_file_base_name
        self.log_level = log_level
        self.quiet = quiet
        self.log_format = log_format


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {
                'summary': obj.summary,
                'description': obj.description
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)


class Event:
    def __init__(
            self,
            summary: str,
            description: str):
        self.summary = summary
        self.description = description

    def to_json(self):
        return json.dumps(self.__dict__, cls=EventEncoder)
