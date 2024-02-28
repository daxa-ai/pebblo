import os
from pebblo.app.utils.utils import get_full_path
from pebblo.app.libs.logger import logger
from abc import ABC, abstractmethod
import sys
import logging


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
            self.errors.append("Error: Host must be a string")
        try:
            port = int(port)
            if not (0 < port <= 65535):
                self.errors.append("Error: Port must be between 1 and 65535")
        except ValueError:
            self.errors.append("Error: Port must be an integer")


class LoggingConfig(ConfigValidator):
    def validate(self):
        level = self.config.get("level", "").upper()
        if level not in logging._nameToLevel:
            self.errors.append("Error: Unsupported logLevel specified in the configuration")


class ReportsConfig(ConfigValidator):
    def validate(self):
        format_ = self.config.get("format")
        renderer = self.config.get("renderer")
        output_dir = self.config.get("outputDir")

        if format_ not in ["pdf"]:
            self.errors.append("Error: Unsupported format specified in the configuration")
        if renderer not in ["weasyprint", "xhtml2pdf"]:
            self.errors.append("Error: Unsupported renderer specified in the configuration")
        if not os.path.exists(get_full_path(output_dir)):
            self.errors.append(f"Error: Output directory '{output_dir}' specified for the reports does not exist")


def validate_config(config_dict):
    validators = {
        "daemon": DaemonConfig,
        "logging": LoggingConfig,
        "reports": ReportsConfig
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