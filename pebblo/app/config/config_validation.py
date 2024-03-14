import logging
import os
import sys
from abc import ABC, abstractmethod

from pebblo.app.libs.logger import logger
from pebblo.app.utils.utils import get_full_path


class ConfigValidator(ABC):
    def __init__(self, config):
        self.config = config
        self.errors = []

    @abstractmethod
    def validate(self):
        pass


class DaemonConfig(ConfigValidator):
    def validate(self):
        host = self.config.get("host")
        port = self.config.get("port")

        if not isinstance(host, str):
            self.errors.append(f"Error: Invalid host '{host}'. Host must be a string.")
        try:
            port = int(port)
            if not (0 < port <= 65535):
                self.errors.append(
                    f"Error: Invalid port '{port}'. Port must be between 1 and 65535."
                )
        except ValueError:
            self.errors.append(
                f"Error: Invalid port value '{port}'. Port must be an integer."
            )


class LoggingConfig(ConfigValidator):
    def validate(self):
        level = self.config.get("level", "").upper()
        if level not in logging._nameToLevel:
            self.errors.append(
                f"Error: Unsupported logLevel '{level}' specified in the configuration"
            )


class ReportsConfig(ConfigValidator):
    def validate(self):
        format_ = self.config.get("format")
        renderer = self.config.get("renderer")
        output_dir = self.config.get("outputDir")

        if format_ not in ["pdf"]:
            self.errors.append(
                f"Error: Unsupported format '{format_}' specified in the configuration"
            )
        if renderer not in ["weasyprint", "xhtml2pdf"]:
            self.errors.append(
                f"Error: Unsupported renderer '{renderer}' specified in the configuration"
            )
        # Check if the output directory exists, create if it doesn't
        if not os.path.exists(get_full_path(str(output_dir))):
            os.makedirs(get_full_path(str(output_dir)), exist_ok=True)


class ClassifierConfig(ConfigValidator):
    def validate(self):
        anonymize_snippets = self.config.get("anonymizeSnippets")
        if not isinstance(anonymize_snippets, bool):
            self.errors.append(
                f"Error: Invalid anonymizeSnippets '{anonymize_snippets}'. anonymizeSnippets must be a boolean."
            )


def validate_config(config_dict):
    validators = {
        "daemon": DaemonConfig,
        "logging": LoggingConfig,
        "reports": ReportsConfig,
        "classifier": ClassifierConfig,
    }

    validation_errors = []

    for section, ValidatorClass in validators.items():
        validator = ValidatorClass(config_dict.get(section, {}))
        validator.validate()
        validation_errors.extend(validator.errors)

    if validation_errors:
        for error in validation_errors:
            logger.error(error)
        sys.exit(1)
