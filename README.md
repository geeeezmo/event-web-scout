# event-web-scout

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/geeeezmo/event-web-scout/ci.yml?label=Build)

![GitHub Latest Pre-Release)](https://img.shields.io/github/v/release/geeeezmo/event-web-scout?include_prereleases&label=pre-release&logo=github)  
![GitHub Latest Release)](https://img.shields.io/github/v/release/geeeezmo/event-web-scout?logo=github)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/geeeezmo/event-web-scout)

![PyPI - Version](https://img.shields.io/pypi/v/event-web-scout?label=PyPI%20version)

Configuration is a JSON with 4 elements:
- `logging` - logging config
  - `level` - logging level (defaults to `ERROR` if not provided)
  - `log_file_base_name` - base name of the logging file (defaults to `event_web_scout`); will be suffixed with the date of the script launch and `.log`
  - `quiet` - sets logging level to `ERROR`
  - `format` - logging message format (defaults to `[%(levelname)s][%(name)s]%(asctime)s - %(message)s`)
- `plugin_entry_points` - list of entry points that will be scanned for plugins
- `plugin_execution` - plugin execution config
  - `timeout_seconds` - how long a plugin is allowed to run for (in seconds); one setting for all plugins; if not provided, 30 seconds is the default
- `plugin_defaults` - default plugin config (overriden by config defined explicitly for each individual plugin); default value is an empty object
- `plugins`- array of configurations for individual plugins; each configuration has 3 properties:
  - `name` - name of the plugin (name of the plugin package)
  - `priority` - priority of plugin execution (lower number = higher priority); plugins with the same priority value will be executed in alphabetical order
  - `enabled` - whether the plugin is enabled
  - `config` - individual plugin configuration; will be passed to the plugin constructor as the first argument


```json
{
  "logging": {
    "level": "INFO",
    "log_file_base_name": "event_web_scout",
    "quiet": false,
    "format": "[%(levelname)s][%(name)s]%(asctime)s - %(message)s"
  },
  "plugin_entry_points": [
    "example_plugins"
  ],
  "plugin_execution": {
    "timeout_seconds": 30
  },
  "plugin_defaults": {
    "priority": 10,
    "enabled": false,
    "config": {
      "google_service_account_token_file": "google_service_account_token.json",
      "google_calendar_id": "<google_calendar_id>"
    }
  },
  "plugins": [
    {
      "name": "example_plugin",
      "priority": 3,
      "enabled": true,
      "config": {
        "example_prop_1": "example_value_1"
      }
    },
    {
      "name": "cool_plugin_1",
      "config": {
        "google_calendar_id": "cool_calendar_id"
      }
    }
  ]
}
```

JSON schema generation was done using these tools:
- [Transform](https://transform.tools/json-to-json-schema)
- [Code Beautify](https://codebeautify.org/json-to-json-schema-generator)
