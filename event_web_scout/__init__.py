from contextlib import ExitStack
from jsonschema import validate
from plugin_interface import PluginInterface
from importlib.metadata import entry_points
import json

class LoadedPlugin():
    def __init__(self, priority: int, name: str, instance: PluginInterface):
        self.priority = priority
        self.name = name
        self.instance = instance

with ExitStack() as stack:
    schema_file = stack.enter_context(open('config_schema.json', 'r'))
    config_schema = json.load(schema_file)

    config_file = stack.enter_context(open('config.json', 'r'))
    config = json.load(config_file)
    plugin_entry_points = config.get('plugin_entry_points', [])
    plugin_configs = config.get('plugins', [])

    for plugin_config in plugin_configs:
        try:
            validate(plugin_config, config_schema)
        except Exception as e:
            print(f'Plugin config validation error: {e}')

    for entry_point in plugin_entry_points:
        discovered_plugins = entry_points(group=entry_point)
        loaded_plugins = []

        print(f'discovered_plugins for entry point {entry_point}: {discovered_plugins}')

        for plugin in discovered_plugins:
            print(f'plugin: {plugin}')
            plugin_config = next((pc for pc in plugin_configs if pc.get('name') == plugin.name), None)
            if plugin_config is not None and plugin_config.get('enabled') is True:
                priority = plugin_config.get('priority', 1)
                loaded_plugin = plugin.load()
                loaded_plugins.append(LoadedPlugin(priority, plugin.name, loaded_plugin))
                print(f'loaded_plugin: {loaded_plugin}; priority: {priority}')

        for plugin in sorted(loaded_plugins, key=lambda p: (p.priority, p.name)):
            print(f'plugin {plugin.name} with priority {plugin.priority}')
            plugin.instance().run()