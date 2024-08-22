import os
import shutil

import pytest

from pebblo.app.config.config_validation import (
    ClassifierConfig,
    DaemonConfig,
    LoggingConfig,
    ReportsConfig,
    validate_config,
)


@pytest.fixture
def setup_and_teardown():
    """
    Create a directory before running the test and delete it after the test is done.
    """
    # Setup: Create directory
    os.makedirs(os.path.expanduser("~/.pebblo_test_"), exist_ok=True)
    yield
    # Teardown: Delete directory
    shutil.rmtree(os.path.expanduser("~/.pebblo_test_"))


def test_daemon_config_validate():
    # Test with valid host and port
    config = {"host": "localhost", "port": "8000"}
    validator = DaemonConfig(config)
    validator.validate()
    assert validator.errors == []

    # Test with invalid host
    config = {"host": 123, "port": "8000"}
    validator = DaemonConfig(config)
    validator.validate()
    assert validator.errors == ["Error: Invalid host '123'. Host must be a string."]

    # Test with invalid port
    config = {"host": "localhost", "port": 70000}
    validator = DaemonConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Invalid port '70000'. Port must be between 1 and 65535."
    ]

    # Test with negative port
    config = {"host": "localhost", "port": -1}
    validator = DaemonConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Invalid port '-1'. Port must be between 1 and 65535."
    ]

    # Test with invalid port using string value
    config = {"host": "localhost", "port": "abc"}
    validator = DaemonConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Invalid port value 'abc'. Port must be an integer."
    ]


def test_logging_config_validate():
    # Test with valid log level
    config = {"level": "info"}
    validator = LoggingConfig(config)
    validator.validate()
    assert validator.errors == []

    # Test with invalid log level
    log_level = "invalid_level"
    config = {"level": log_level}
    validator = LoggingConfig(config)
    validator.validate()
    assert validator.errors == [
        f"Error: Unsupported logLevel '{log_level.upper()}' specified in the configuration"
    ]


def test_reports_config_validate(setup_and_teardown):
    # Test with valid format, renderer, and output directory
    config = {"format": "pdf", "renderer": "xhtml2pdf", "cacheDir": "~/.pebblo_test_"}
    validator = ReportsConfig(config)
    validator.validate()
    assert validator.errors == []

    # Test with invalid format
    config = {"format": "doc", "renderer": "xhtml2pdf", "cacheDir": "~/.pebblo_test_"}
    validator = ReportsConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Unsupported format 'doc' specified in the configuration"
    ]

    # Test with invalid renderer
    config = {
        "format": "pdf",
        "renderer": "invalid_renderer",
        "cacheDir": "~/.pebblo_test_",
    }
    validator = ReportsConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Unsupported renderer 'invalid_renderer' specified in the configuration"
    ]


def test_classifier_config_validate():
    # Test with True value
    config = {"anonymizeSnippets": True}
    validator = ClassifierConfig(config)
    validator.validate()
    assert validator.errors == []

    # Test with False value
    config = {"anonymizeSnippets": False}
    validator = ClassifierConfig(config)
    validator.validate()
    assert validator.errors == []

    # Test with invalid int
    config = {"anonymizeSnippets": 70000}
    validator = ClassifierConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Invalid anonymizeSnippets '70000'. anonymizeSnippets must be a boolean."
    ]

    # Test with invalid str
    config = {"anonymizeSnippets": "abc"}
    validator = ClassifierConfig(config)
    validator.validate()
    assert validator.errors == [
        "Error: Invalid anonymizeSnippets 'abc'. anonymizeSnippets must be a boolean."
    ]


def test_validate_config(setup_and_teardown):
    # Test with valid configuration
    config = {
        "daemon": {"host": "localhost", "port": "8000"},
        "logging": {"level": "info"},
        "reports": {
            "format": "pdf",
            "renderer": "xhtml2pdf",
            "cacheDir": "~/.pebblo_test_",
        },
        "classifier": {
            "anonymizeSnippets": True,
        },
        "storage":{
            "type": "file"
        },
    }
    validate_config(config)
    # If the configuration is valid, validate_config should not raise any exceptions

    # Test with invalid configuration
    config = {
        "daemon": {"host": 123, "port": "8000"},
        "logging": {"level": "invalid_level"},
        "reports": {
            "format": "doc",
            "renderer": "xhtml2pdf",
            "cacheDir": "~/.pebblo_test_",
        },
        "classifier": {
            "anonymizeSnippets": "abc",
        },
    }
    with pytest.raises(SystemExit):
        validate_config(config)
    # If the configuration is invalid, validate_config should raise a SystemExit exception
