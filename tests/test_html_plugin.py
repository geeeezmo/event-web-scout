__spec__ = "test_html_plugin"

import logging
import os
from contextlib import ExitStack

import pytest
# from bs4 import BeautifulSoup
from pytest_httpserver import HTTPServer

from event_web_scout import init, get_loaded_plugins, exec_plugin, LoadedPlugin
from event_web_scout.models import Event
from test_utils import install_dependencies, random_string


@pytest.fixture(scope="module", autouse=True)
def install_deps(request):
    result = install_dependencies(['plugins/html-plugin'], ['pytest_httpserver==1.0.10'])
    # Yield control back to the test
    yield result


init(config_file_name='../tests/config/html_plugin_config.json')
loaded_plugins = get_loaded_plugins()


def test_html_plugin_200_response(install_deps, httpserver: HTTPServer):
    """HTML plugin should parse an HTML page and create an event from document title and body
    when the server responded with 200 OK"""
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    plugin_config_with_mock_url = dict(plugin.config, **{"base_url": httpserver.url_for("/test-html-plugin")})
    plugin.config.update(plugin_config_with_mock_url)
    print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')

    with ExitStack() as stack:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            html_file = stack.enter_context(open(os.path.join(script_dir, 'html/basic.html'), 'r'))
            expected_html_response = html_file.read()
            (httpserver
             .expect_request("/test-html-plugin")
             .respond_with_data(expected_html_response, status=200, content_type="text/html"))

            response = exec_plugin(plugin)

            if isinstance(response, list):
                assert len(response) == 1
                event = response[0]
                assert (isinstance(event, Event) and
                        event.to_json() == '{"summary": "Mock document title", "description": "Mock document body"}')

        except FileNotFoundError as e:
            pytest.fail(f'Required HTML file not found: {e}')


@pytest.mark.parametrize("http_code", [301, 302, 307, 308])
def test_html_plugin_3xx_response(install_deps, httpserver: HTTPServer, http_code: int):
    """HTML plugin should follow redirects and parse an HTML page and create an event from
    document title and body when the server responded with one of the 3xx Moved HTTP codes"""
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    plugin_config_with_mock_url = dict(plugin.config, **{"base_url": httpserver.url_for("/test-html-plugin")})
    plugin.config.update(plugin_config_with_mock_url)
    print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')

    with (ExitStack() as stack):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            html_file = stack.enter_context(open(os.path.join(script_dir, 'html/basic.html'), 'r'))
            expected_html_response = html_file.read()

            new_url = random_string()
            (httpserver
             .expect_request("/test-html-plugin")
             .respond_with_data(status=http_code, headers=[("Location", f'/{new_url}')]))
            (httpserver
             .expect_request(f'/{new_url}')
             .respond_with_data(expected_html_response, status=200, content_type="text/html"))

            response = exec_plugin(plugin)

            if isinstance(response, list):
                assert len(response) == 1
                event = response[0]
                assert (isinstance(event, Event) and
                        event.to_json() == '{"summary": "Mock document title", "description": "Mock document body"}')

        except FileNotFoundError as e:
            pytest.fail(f'Required HTML file not found: {e}')


def test_html_plugin_404_response(install_deps, httpserver: HTTPServer):
    """HTML plugin should return an empty list of events when the server responded with 404 Not Found"""
    assert len(loaded_plugins) == 1

    plugin = loaded_plugins[0]
    plugin_config_with_mock_url = dict(plugin.config, **{"base_url": httpserver.url_for("/test-html-plugin")})
    plugin.config.update(plugin_config_with_mock_url)
    print(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')
    logging.info(f'loaded plugin \'{plugin.name}\' with priority {plugin.priority}')

    (httpserver
     .expect_request("/test-html-plugin")
     .respond_with_data(status=404, content_type="text/html"))

    response = exec_plugin(plugin)

    if isinstance(response, list):
        assert len(response) == 0
