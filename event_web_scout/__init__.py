from contextlib import ExitStack
from jsonschema import validate
from .plugin_interface import PluginInterface
from importlib.metadata import entry_points
import json
import os

class LoadedPlugin():
    def __init__(self, priority: int, name: str, config: object, _class: PluginInterface):
        self.priority = priority
        self.name = name
        self.config = config
        self._class = _class

    def new_instance(self) -> PluginInterface:
        return self._class(self.config)
        
loaded_plugins = []

with ExitStack() as stack:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = stack.enter_context(open(os.path.join(script_dir, 'config_schema.json'), 'r'))
    config_schema = json.load(schema_file)

    config_file = stack.enter_context(open(os.path.join(script_dir, 'config.json'), 'r'))
    config = json.load(config_file)
    plugin_entry_points = config.get('plugin_entry_points', [])

    # Merge defaults with each plugin's configuration
    # Track plugin names, and if non unique name is provided in config, raise a ValueError
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

    try:
        validate(instance=config, schema=config_schema)
    except Exception as e:
        print(f'Plugin config validation error: {e}')

    for entry_point in plugin_entry_points:
        discovered_plugins = entry_points(group=entry_point)

        # print(f'discovered_plugins for entry point {entry_point}: {discovered_plugins}')

        for plugin in discovered_plugins:
            # print(f'discovered plugin: {plugin}')
            plugin_config = next((pc for pc in plugin_configs if pc.get('name') == plugin.name), None)
            # print(f'plugin_config: {plugin_config}')
            if plugin_config is not None and plugin_config.get('enabled') is True:
                priority = plugin_config.get('priority')
                plugin_class = plugin.load()
                loaded_plugin = LoadedPlugin(priority, plugin.name, plugin_config.get('config'), plugin_class)
                loaded_plugins.append(loaded_plugin)
                # print(f'loaded_plugin: {loaded_plugin.name}; priority: {priority}')

def exec_loaded_plugins():
    for plugin in sorted(loaded_plugins, key=lambda p: (p.priority, p.name)):
        # print(f'plugin {plugin.name} with priority {plugin.priority}')
        plugin.new_instance().run()

__all__ = ['loaded_plugins', 'exec_loaded_plugins']