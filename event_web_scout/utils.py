from . import LoggingConfig
from datetime import datetime
from dateutil import tz
from typeguard import typechecked
import logging
import os

LOG_FORMAT = '[%(levelname)s][%(name)s]%(asctime)s - %(message)s'
TIMEZONE = tz.gettz('Europe/Helsinki')


@typechecked
def init_loggers(config: LoggingConfig):
    log_level = logging.ERROR
    if not config.quiet and config.level is not None:
        log_level = config.level.upper()
    log_format = config.format or LOG_FORMAT
    logging.basicConfig(format=log_format, level=log_level)
    formatter = logging.Formatter(log_format)

    today = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    log_file_name = config.log_file_base_name or 'event_web_scout'
    log_file_path = os.path.join(config.log_dir, 'log', f'{log_file_name}_{today}.log')
    print(f'log_file_path = {log_file_path}')
    print(f'log_level = {log_level}')
    print(f'log_format = {log_format}')
    create_dir(log_file_path)
    # Create a file handler
    file_handler = logging.handlers.WatchedFileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(file_handler)
    root.addHandler(console_handler)


@typechecked
def create_dir(path: str):
    try:
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        pass
