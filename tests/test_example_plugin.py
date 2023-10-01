from event_web_scout import init, get_loaded_plugins, exec_plugin
from func_timeout import exceptions
import pytest
import subprocess

@pytest.fixture(scope="session")
def install_dependencies():
    # Define the dependencies to install
    dependencies_to_install = [
        '.',
        'plugins/example-plugin'
    ]

    # Install the dependencies using pip
    for dependency in dependencies_to_install:
        print(f'installing {dependency}')
        subprocess.run(['pip3', 'install', '-e', dependency])
    
    # Yield control back to the test
    yield

    # Clean up (optional): Uninstall the dependencies, if needed
    # for dependency in dependencies_to_install:
    #     subprocess.run(['pip3', 'uninstall', '-y', dependency])

init()
loaded_plugins = get_loaded_plugins()

def test_stable_example_plugin(install_dependencies):
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    print(f'plugin {plugin.name} with priority {plugin.priority}')
    exec_plugin(plugin)

def test_timeout_example_plugin(install_dependencies):    
    assert len(loaded_plugins) == 1

    with pytest.raises(exceptions.FunctionTimedOut) as fto:
        plugin = loaded_plugins[0]
        print(f'plugin {plugin.name} with priority {plugin.priority}')
        exec_plugin(plugin, forceTimeout = 2)

    assert fto.value.timedOutAfter == 2