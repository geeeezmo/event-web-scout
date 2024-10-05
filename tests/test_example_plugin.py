import logging
import pytest
from func_timeout import exceptions

from event_web_scout import init, get_loaded_plugins, exec_plugin
from test_utils import install_dependencies


@pytest.fixture(scope="module", autouse=True)
def install_deps(request):
    result = install_dependencies(['plugins/example-plugin'])
    # Yield control back to the test
    yield result


init(config_file_name='../tests/config/config_with_plugin_sleep_time.json')
loaded_plugins = get_loaded_plugins()


@pytest.mark.slow
def test_example_plugin_loading(install_deps):
    """Plugin should be loaded correctly"""
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')


@pytest.mark.slow
def test_fast_example_plugin(install_deps):
    """Plugin should be executed and exit without errors within the configured time limit"""
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    exec_plugin(plugin)


@pytest.mark.slow
def test_timeout_example_plugin(install_deps):
    """Plugin execution should be timed out after the configured duration"""
    assert len(loaded_plugins) == 1

    with pytest.raises(exceptions.FunctionTimedOut) as fto:
        plugin = loaded_plugins[0]
        print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
        logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
        exec_plugin(plugin, forceTimeout=2)

    assert fto.value.timedOutAfter == 2
