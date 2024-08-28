import logging
import os
import sys
from abc import ABC, abstractmethod

from pebblo.app.enums.common import DBStorageTypes, StorageTypes


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


class StorageConfig(ConfigValidator):
    def validate(self):
        storage_type = self.config.get("type")
        valid_storage_types = [storage_type.value for storage_type in StorageTypes]
        if storage_type not in valid_storage_types:
            self.errors.append(
                f"Error: Unsupported storage type '{storage_type}' specified in the configuration."
                f"Valid values are {valid_storage_types}"
            )

        if storage_type == StorageTypes.DATABASE.value:
            db_type = self.config.get("db")
            default_location = self.config.get("location")
            db_name = self.config.get("name")

            valid_db_types = [storage_type.value for storage_type in DBStorageTypes]
            if db_type not in valid_db_types:
                self.errors.append(
                    f"Error: Unsupported db type '{db_type}' specified in the configuration."
                    f"Valid values are {valid_db_types}"
                )

            # db_name should be in string
            if not isinstance(db_name, str):
                self.errors.append(
                    f"Error: Unsupported db name '{db_name} specified in the configuration"
                    f"String values are allowed only"
                )

            # Check if the output directory exists, create if it doesn't
            if not os.path.exists(expand_path(str(default_location))):
                os.makedirs(expand_path(str(default_location)), exist_ok=True)


def expand_path(file_path: str) -> str:
    # Expand user (~) and environment variables
    expanded_path = os.path.expanduser(file_path)
    expanded_path = os.path.expandvars(expanded_path)

    # Convert to absolute path
    absolute_path = os.path.abspath(expanded_path)

    return absolute_path


class ReportsConfig(ConfigValidator):
    def validate(self):
        format_ = self.config.get("format")
        renderer = self.config.get("renderer")
        cache_dir = self.config.get("cacheDir")

        if format_ not in ["pdf"]:
            self.errors.append(
                f"Error: Unsupported format '{format_}' specified in the configuration"
            )
        if renderer not in ["weasyprint", "xhtml2pdf"]:
            self.errors.append(
                f"Error: Unsupported renderer '{renderer}' specified in the configuration"
            )
        # Check if the output directory exists, create if it doesn't
        if not os.path.exists(expand_path(str(cache_dir))):
            os.makedirs(expand_path(str(cache_dir)), exist_ok=True)

    @staticmethod
    def validate_input(input_dict):
        deprecate_error = "DeprecationWarning: 'outputDir' in config is deprecated, use 'cacheDir' instead"
        dirs = input_dict.get("reports").keys()
        if "cacheDir" in dirs and "outputDir" in dirs:
            raise Exception(
                f"Either 'cacheDir' or 'outputDir' should be there in config \n{deprecate_error}"
            )

        if "outputDir" in dirs:
            print(deprecate_error)
            input_dict["reports"]["cacheDir"] = input_dict["reports"]["outputDir"]
            input_dict["reports"].pop("outputDir")
        return input_dict


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
        "storage": StorageConfig,
    }

    validation_errors = []

    for section, ValidatorClass in validators.items():
        validator = ValidatorClass(config_dict.get(section, {}))
        validator.validate()
        validation_errors.extend(validator.errors)

    if validation_errors:
        for error in validation_errors:
            print(error)
        sys.exit(1)


def validate_input(input_dict):
    """This function is used to validate input of config file"""
    validators = {
        "reports": ReportsConfig,
    }

    validation_errors = []

    output_dict = input_dict
    for section, ValidatorClass in validators.items():
        validator = ValidatorClass(input_dict.get(section, {}))
        output_dict = validator.validate_input(input_dict)
        validation_errors.extend(validator.errors)

    if validation_errors:
        for error in validation_errors:
            print(error)
        sys.exit(1)

    return output_dict
