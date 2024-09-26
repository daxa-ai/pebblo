import importlib.util
import logging
import os
from typing import Optional, Union

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings

from pebblo.app.config import utils
from pebblo.app.config.utils import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_MAX_FILE_SIZE,
    dir_path,
    expand_path,
    update_anonymize_snippets_exists,
)
from pebblo.app.enums.common import (
    ClassificationMode,
    DBStorageTypes,
    ReportFormat,
    ReportLibraries,
    StorageTypes,
)


# Port BaseModel
class DaemonConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)

    @field_validator("port")
    @classmethod
    def check_port_validity(cls, port: int) -> int:
        # check to validate port should be between 0 and 65535
        if not (0 < port <= 65535):
            raise ValueError(
                f"Error: Invalid port '{port}'. Port must be between 1 and 65535."
            )
        return port


# Logging BaseModel
class LoggingConfig(BaseSettings):
    level: str = Field(default=DEFAULT_LOG_LEVEL)
    file: str = Field(default=DEFAULT_LOG_FILE)
    maxFileSize: int = Field(default=DEFAULT_LOG_MAX_FILE_SIZE)
    backupCount: int = Field(default=DEFAULT_LOG_BACKUP_COUNT)

    @field_validator("level")
    @classmethod
    def validate_logging_level_value(cls, level: str) -> str:
        # check to validate level entry
        if level.upper() not in logging._nameToLevel:
            raise ValueError(
                f"Error: Unsupported logLevel '{level}' specified in the configuration"
            )
        return level


# Report BaseModel
class ReportConfig(BaseSettings):
    format: str = Field(default=ReportFormat.PDF.value)
    renderer: str = Field(default=ReportLibraries.XHTML2PDF.value)
    cacheDir: str = Field(default=str(dir_path))
    anonymizeSnippets: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
    def validate_report_config_model(cls, data: dict) -> dict:
        # check to validate reports config model entries
        deprecate_error = "DeprecationWarning: 'outputDir' in config is deprecated, use 'cacheDir' instead"
        report_config_key = data.keys()
        if "cacheDir" in report_config_key and "outputDir" in report_config_key:
            # check to validate both `cacheDir` and `outputDir` should not be there is in reports config
            raise Exception(
                f"Either 'cacheDir' or 'outputDir' should be there in config \n{deprecate_error}"
            )

        if "outputDir" in report_config_key:
            # if `outputDir` is there in reports config, give deprecation message
            print(deprecate_error)
            data["cacheDir"] = data["outputDir"]
            data.pop("outputDir")
        return data

    @field_validator("format")
    @classmethod
    def validate_format_value(cls, format_: str) -> str:
        # check to validate format value in reports config model
        valid_format_values = [format_type.value for format_type in ReportFormat]
        if format_ not in valid_format_values:
            raise ValueError(
                f"Error: Unsupported format type '{format_}' specified in the configuration. Valid values are {valid_format_values}"
            )
        return format_

    @field_validator("renderer")
    @classmethod
    def validate_renderer_value(cls, renderer: str) -> str:
        # check to validate renderer value in reports config model
        valid_renderer_values = [
            renderer_value.value for renderer_value in ReportLibraries
        ]
        if renderer not in valid_renderer_values:
            raise ValueError(
                f"Error: Unsupported renderer value '{renderer}' specified in the configuration. Valid values are {valid_renderer_values}"
            )
        if renderer == "weasyprint":
            # Check if weasyprint is installed
            if importlib.util.find_spec("weasyprint") is None:
                error = """Error: `renderer: weasyprint` was specified, but weasyprint was not found.
                Follow documentation for more details - https://daxa-ai.github.io/pebblo/installation"""
                raise ValueError(error)
        return renderer

    @field_validator("cacheDir")
    @classmethod
    def check_if_cache_dir_exists(cls, cache_dir: str) -> str:
        # Check if the output directory exists, create if it doesn't
        if not os.path.exists(expand_path(str(cache_dir))):
            os.makedirs(expand_path(str(cache_dir)), exist_ok=True)
        return cache_dir

    @field_validator("anonymizeSnippets")
    @classmethod
    def validate_anonymize_snippets(cls, anonymize_snippets: bool) -> bool:
        # check to validate anonymizeSnippets should be boolean
        if anonymize_snippets is not None:
            update_anonymize_snippets_exists()
            if not isinstance(anonymize_snippets, bool):
                raise ValueError(
                    f"Error: Invalid anonymizeSnippets '{anonymize_snippets}'. anonymizeSnippets must be a boolean."
                )
        return anonymize_snippets


# Classifier BaseModel
class ClassifierConfig(BaseSettings):
    mode: str = Field(default=ClassificationMode.ALL.value)
    anonymizeSnippets: Optional[bool] = None

    @field_validator("mode")
    @classmethod
    def validate_mode_value(cls, mode: str) -> str:
        valid_classification_modes = [
            classification_mode.value for classification_mode in ClassificationMode
        ]
        if mode not in valid_classification_modes:
            raise ValueError(
                f"Error: Unsupported classifier mode '{mode}' specified in the configuration. Valid values are {valid_classification_modes}"
            )
        return mode

    @field_validator("anonymizeSnippets")
    @classmethod
    def validate_anonymize_snippets(cls, anonymize_snippets: bool) -> bool:
        # if `anonymizeSnippets` is there in classifier config, give deprecation message
        if anonymize_snippets is not None:
            print(
                "DeprecationWarning: 'anonymizeSnippets' in classifier is deprecated, use 'anonymizeSnippets' in reports instead"
            )
            # check if anonymizeSnippet is already there in Reports Config,it should throw error
            if utils.anonymize_snippets_exists:
                raise ValueError(
                    "'anonymizeSnippets' should be either in classifier or reports"
                )
            # check to validate anonymizeSnippets should be boolean
            if not isinstance(anonymize_snippets, bool):
                raise ValueError(
                    f"Error: Invalid anonymizeSnippets '{anonymize_snippets}'. anonymizeSnippets must be a boolean."
                )
            return anonymize_snippets


# Storage Basemodel
class StorageConfig(BaseSettings):
    type: str = Field(default=StorageTypes.FILE.value)
    db: Union[str, None] = Field(default=DBStorageTypes.SQLITE.value)
    location: Union[str, None] = Field(default=str(dir_path))
    name: Union[str, None] = Field(default=str("pebblo"))
    # This is default value for current version(0.1.18), it needs to be changed in next version to db.

    @model_validator(mode="before")
    @classmethod
    def validate_storage_config_model(cls, data: dict) -> dict:
        storage_type = data.get("type")
        valid_storage_types = [storage_type.value for storage_type in StorageTypes]
        # check to validate valid storage type
        if storage_type not in valid_storage_types:
            raise ValueError(
                f"Error: Unsupported storage type '{storage_type}' specified in the configuration."
                f"Valid values are {valid_storage_types}"
            )
        if storage_type == StorageTypes.FILE.value:
            print(
                f"DeprecationWarning: '{StorageTypes.FILE.value}' in storage type will be deprecated from next release, use '{StorageTypes.DATABASE.value}' instead"
            )
        if storage_type == StorageTypes.DATABASE.value:
            db_type = data.get("db")
            if db_type is not None:
                valid_db_types = [storage_type.value for storage_type in DBStorageTypes]
                # check to validate valid db type
                if db_type not in valid_db_types:
                    raise ValueError(
                        f"Error: Unsupported db type '{db_type}' specified in the configuration."
                        f"Valid values are {valid_db_types}"
                    )

            default_location = data.get("location")
            if default_location is None:
                default_location = str(dir_path)
            # Check if the default output location directory exists, create if it doesn't
            if not os.path.exists(expand_path(str(default_location))):
                os.makedirs(expand_path(str(default_location)), exist_ok=True)

            db_name = data.get("name")
            if db_name is not None:
                # check to validate db_name should be in string
                if not isinstance(db_name, str):
                    raise ValueError(
                        f"Error: Unsupported db name '{db_name} specified in the configuration. "
                        f"String values are allowed only"
                    )
        return data


# ConfigFile BaseModel
class Config(BaseSettings):
    daemon: DaemonConfig
    reports: ReportConfig
    classifier: ClassifierConfig
    logging: LoggingConfig
    storage: StorageConfig
