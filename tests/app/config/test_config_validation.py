import pytest

from pebblo.app.config.models import (
    Config,
)

config_json = {
    "daemon": {"port": 8000, "host": "localhost"},
    "logging": {"level": "info"},
    "reports": {
        "format": "pdf",
        "renderer": "xhtml2pdf",
        "cacheDir": "~/.pebblo",
        "anonymizeSnippets": True,
    },
    "classifier": {"mode": "all"},
    "storage": {"type": "file"},
}


def test_with_valid_values():
    valid_data = Config.parse_obj(config_json)
    assert valid_data == Config(**config_json)


def test_daemon_config_validate_invalid_port():
    config_json.update({"daemon": {"host": "localhost", "port": "12345678"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """daemon.port
  Value error, Error: Invalid port '12345678'. Port must be between 1 and 65535."""
    assert error_msg in str(err_msg.value)


def test_daemon_config_validate_invalid_host():
    config_json.update({"daemon": {"host": 123, "port": "8000"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """daemon.host
  Input should be a valid string [type=string_type, input_value=123, input_type=int]"""
    assert error_msg in str(err_msg.value)


def test_daemon_config_validate_invalid_values():
    config_json.update({"daemon": {"host": 123, "port": 12345678}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """daemon.host
  Input should be a valid string [type=string_type, input_value=123, input_type=int]
    For further information visit https://errors.pydantic.dev/2.8/v/string_type
daemon.port
  Value error, Error: Invalid port '12345678'. Port must be between 1 and 65535."""
    assert error_msg in str(err_msg.value)


def test_logging_config_validate_invalid_log_level():
    config_json.update({"logging": {"level": "invalid_level"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """logging.level
  Value error, Error: Unsupported logLevel 'invalid_level' specified in the configuration"""
    assert error_msg in str(err_msg.value)


def test_classifier_config_validate_invalid_mode():
    config_json.update({"classifier": {"mode": "123"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """classifier.mode
  Value error, Error: Unsupported classifier mode '123' specified in the configuration. Valid values are ['all', 'entity', 'topic'] [type=value_error, input_value='123', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_classifier_config_validate_invalid_anonymize_snippets():
    config_json.update({"classifier": {"mode": "all", "anonymizeSnippets": "123"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """classifier.anonymizeSnippets
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='123', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_classifier_config_validate_invalid_values():
    config_json.update(
        {"classifier": {"mode": "false_value", "anonymizeSnippets": "123"}}
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """classifier.mode
  Value error, Error: Unsupported classifier mode 'false_value' specified in the configuration. Valid values are ['all', 'entity', 'topic'] [type=value_error, input_value='false_value', input_type=str]
    For further information visit https://errors.pydantic.dev/2.8/v/value_error
classifier.anonymizeSnippets
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='123', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_report_config_validate_both_cache_and_output_dir():
    config_json.update(
        {
            "classifier": {"mode": "all"},
            "reports": {
                "format": "pdf",
                "renderer": "xhtml2pdf",
                "outputDir": "~/.pebblo",
                "cacheDir": "~/.pebblo",
                "anonymizeSnippets": False,
            },
        }
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = "Either 'cacheDir' or 'outputDir' should be there in config \nDeprecationWarning: 'outputDir' in config is deprecated, use 'cacheDir' instead"
    assert error_msg in str(err_msg.value.args[0])


def test_report_config_validate_invalid_format_value():
    config_json.update(
        {
            "reports": {
                "format": "wrong_format",
                "renderer": "xhtml2pdf",
                "cacheDir": "~/.pebblo",
                "anonymizeSnippets": False,
            }
        }
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """reports.format
  Value error, Error: Unsupported format type 'wrong_format' specified in the configuration. Valid values are ['pdf'] [type=value_error, input_value='wrong_format', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_report_config_validate_invalid_renderer_value():
    config_json.update(
        {
            "reports": {
                "format": "pdf",
                "renderer": "wrong_value",
                "cacheDir": "~/.pebblo",
                "anonymizeSnippets": False,
            }
        }
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """reports.renderer
  Value error, Error: Unsupported renderer value 'wrong_value' specified in the configuration. Valid values are ['xhtml2pdf', 'weasyprint'] [type=value_error, input_value='wrong_value', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_report_config_validate_weasyprint_renderer_value():
    config_json.update(
        {
            "reports": {
                "format": "pdf",
                "renderer": "weasyprint",
                "cacheDir": "~/.pebblo",
            }
        }
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """reports.renderer
  Value error, Error: `renderer: weasyprint` was specified, but weasyprint was not found.
                Follow documentation for more details - https://daxa-ai.github.io/pebblo/installation [type=value_error, input_value='weasyprint', input_type=str]"""
    assert error_msg in str(err_msg.value)


def test_report_config_validate_with_invalid_anonymize_snippets():
    config_json.update(
        {
            "reports": {
                "format": "pdf",
                "renderer": "xhtml2pdf",
                "cacheDir": "~/.pebblo",
                "anonymizeSnippets": 123,
            }
        }
    )
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """reports.anonymizeSnippets
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value=123, input_type=int]"""
    assert error_msg in str(err_msg.value)


def test_storage_config_validate_invalid_type_value():
    config_json.update({"storage": {"type": "wrong_value"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """storage
  Value error, Error: Unsupported storage type 'wrong_value' specified in the configuration.Valid values are ['file', 'db'] [type=value_error, input_value={'type': 'wrong_value'}, input_type=dict]"""
    assert error_msg in str(err_msg.value)


def test_storage_config_validate_db_type_value():
    config_json.update({"storage": {"type": "db", "db": "test_db"}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """storage
  Value error, Error: Unsupported db type 'test_db' specified in the configuration.Valid values are ['sqlite'] [type=value_error, input_value={'type': 'db', 'db': 'test_db'}, input_type=dict]"""
    assert error_msg in str(err_msg.value)

    config_json.update({"storage": {"type": "db", "db": "sqlite", "name": 123}})
    with pytest.raises(Exception) as err_msg:
        Config.parse_obj(config_json)
    error_msg = """storage
  Value error, Error: Unsupported db name '123 specified in the configuration. String values are allowed only [type=value_error, input_value={'type': 'db', 'db': 'sqlite', 'name': 123}, input_type=dict]"""
    assert error_msg in str(err_msg.value)
