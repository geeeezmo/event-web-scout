from contextlib import ExitStack
from jsonschema import validate
from .models import LoadedPlugin, LoggingConfig
from .utils import init_loggers
from func_timeout import func_set_timeout
from importlib.metadata import entry_points
from typeguard import typechecked
import json
import logging
import logging.handlers
import os
import sys

loaded_plugins: list[LoadedPlugin] = []


@typechecked
def init(config_file: str = 'config.json', config_schema_file: str = 'config_schema.json'):
    with ExitStack() as stack:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            schema_file = stack.enter_context(open(os.path.join(script_dir, config_schema_file), 'r'))
            config_schema = json.load(schema_file)

            config_file = stack.enter_context(open(os.path.join(script_dir, config_file), 'r'))
            config = json.load(config_file)
        except FileNotFoundError as e:
            logging.error(f'File does not exist: {e}')
            sys.exit(1000)
        except json.JSONDecodeError as jde:
            logging.error(f'Could not decode JSON: {jde}')
            sys.exit(1010)
        except TypeError as te:
            logging.error(f'Could not decode JSON: {te}')
            sys.exit(1020)

        validate_config(config_schema, config)

        plugin_entry_points = config.get('plugin_entry_points', [])

        # Merge defaults with each plugin's configuration
        # Track plugin names, and if non-unique name is provided in config, raise a ValueError
        plugin_names = set()
        for plugin_config in config.get('plugins', []):
            if plugin_config["name"] in plugin_names:
                raise ValueError(f'Non-unique plugin name: "{plugin_config["name"]}"')
            else:
                plugin_names.add(plugin_config["name"])
                merged_config = dict(config.get('plugin_defaults', {}), **plugin_config)
                # Replace the original plugin configuration with the merged one
                plugin_config.clear()
                plugin_config.update(merged_config)

        plugin_configs = config.get('plugins', [])
        # print(f'plugin_configs: {plugin_configs}')

        # validate config again after merging individual plugin configs with the defaults
        validate_config(config_schema, config)

        logging_config_json = config.get('logging', {})
        logging_config = LoggingConfig(
            log_dir=script_dir,
            log_file_base_name=logging_config_json.get('log_file_base_name'),
            level=logging_config_json.get('level'),
            quiet=bool(logging_config_json.get('quiet')),
            format=logging_config_json.get('format')
        )

        # initialize loggers using logging config
        init_loggers(logging_config)

        # iterate over plugin entry points, create an instance for each of them
        # and put into the list of loaded plugins
        for entry_point in plugin_entry_points:
            discovered_plugins = entry_points(group=entry_point)

            logging.info(f'discovered_plugins for entry point {entry_point}: {discovered_plugins}')

            for plugin in discovered_plugins:
                # print(f'discovered plugin: {plugin}')
                plugin_config = next((pc for pc in plugin_configs if pc.get('name') == plugin.name), None)
                # print(f'plugin_config: {plugin_config}')
                if plugin_config is not None and plugin_config.get('enabled') is True:
                    priority = plugin_config.get('priority')
                    plugin_class = plugin.load()
                    loaded_plugin = LoadedPlugin(priority, plugin.name, plugin_config.get('config', {}), plugin_class)
                    loaded_plugins.append(loaded_plugin)
                    print(f'loaded_plugin: {loaded_plugin.name}; priority: {priority}')
                    logging.info(f'loaded_plugin: {loaded_plugin.name}; priority: {priority}')


def validate_config(schema: object, config: object):
    try:
        validate(instance=config, schema=schema)
    except Exception as e:
        logging.error(f'Config validation error: {e}')
        sys.exit(1030)


@typechecked
def get_loaded_plugins() -> list[LoadedPlugin]:
    return sorted(loaded_plugins, key=lambda p: (p.priority, p.name))


@func_set_timeout(10, allowOverride=True)
@typechecked
def exec_plugin(plugin: LoadedPlugin):
    """Execute plugin's run method. Default timeout is 10 seconds, but can be overriden by config"""
    logging.info(f'plugin {plugin.name} with priority {plugin.priority}')
    plugin.new_instance().run()


__all__ = [
    'LoadedPlugin',
    'LoggingConfig',
    'get_loaded_plugins'
]