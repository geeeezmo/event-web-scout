from event_web_scout import init
import pytest


def test_missing_config_schema_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        init(config_schema_file_name='missing_schema_file.json')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1000


def test_missing_config_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        init(config_file_name='missing_file.json')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1000


def test_invalid_config_schema_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        init(config_schema_file_name='../tests/invalid_config_schema.json')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1010


def test_invalid_config_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        init(config_file_name='../tests/invalid_config.json')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1010


def test_config_file_schema_mismatch():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        init(config_file_name='../tests/config_with_schema_mismatch.json')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1030
