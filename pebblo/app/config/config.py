import pathlib
from contextvars import ContextVar
from typing import Tuple, Union

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings

from pebblo.app.config.config_validation import validate_config, validate_input
from pebblo.app.enums.common import DBStorageTypes, StorageTypes

# Default config value
dir_path = pathlib.Path().absolute()


# Port BaseModel
class PortConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)


# Report BaseModel
class ReportConfig(BaseSettings):
    format: str = Field(default="pdf")
    renderer: str = Field(default="xhtml2pdf")
    cacheDir: str = Field(default=str(dir_path))


# Logging Defaults
DEFAULT_LOGGER_NAME = "pebblo"
DEFAULT_LOG_MAX_FILE_SIZE = 8 * 1024 * 1024
DEFAULT_LOG_BACKUP_COUNT = 3
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE_PATH = "/tmp/logs"
DEFAULT_LOG_FILE = f"{DEFAULT_LOG_FILE_PATH}/{DEFAULT_LOGGER_NAME}.log"


# Logging BaseModel
class LoggingConfig(BaseSettings):
    level: str = Field(default=DEFAULT_LOG_LEVEL)
    file: str = Field(default=DEFAULT_LOG_FILE)
    maxFileSize: int = Field(default=DEFAULT_LOG_MAX_FILE_SIZE)
    backupCount: int = Field(default=DEFAULT_LOG_BACKUP_COUNT)


class ClassifierConfig(BaseSettings):
    anonymizeSnippets: bool = Field(default=True)


class StorageConfig(BaseSettings):
    type: str = Field(default=StorageTypes.FILE.value)
    db: Union[str, None] = Field(default=DBStorageTypes.SQLITE.value)
    location: Union[str, None] = Field(default=str(dir_path))
    name: Union[str, None] = Field(default=str("pebblo"))
    # This is default value for current version(0.1.18), it needs to be changed in next version to db.


# ConfigFile BaseModel
class Config(BaseSettings):
    daemon: PortConfig
    reports: ReportConfig
    logging: LoggingConfig
    classifier: ClassifierConfig
    storage: StorageConfig


var_server_config: ContextVar[Config] = ContextVar("server_config", default=None)
var_server_config_dict: ContextVar[dict] = ContextVar("server_config_dict", default={})


def load_config(path: str) -> Tuple[dict, Config]:
    try:
        # If Path does not exist in command, set default config value
        conf_obj = Config(
            daemon=PortConfig(host="localhost", port=8000),
            reports=ReportConfig(
                format="pdf", renderer="xhtml2pdf", cacheDir="~/.pebblo"
            ),
            logging=LoggingConfig(),
            classifier=ClassifierConfig(anonymizeSnippets=False),
            storage=StorageConfig(type="file", db=None),
            # for now, a default storage type is FILE, but in the next release DB will be the default storage type.
        )
        if not path:
            # Setting Default config details
            return conf_obj.dict(), conf_obj

        # If Path exist, set config value
        try:
            with open(path, "r") as output:
                cred_yaml = yaml.safe_load(output)
                cred_yaml = validate_input(cred_yaml)

                # Replace missing fields with default values
                for key in conf_obj.dict().keys():
                    if key not in cred_yaml:
                        cred_yaml[key] = conf_obj.dict()[key]
                parsed_config = Config.parse_obj(cred_yaml)
                config_dict = parsed_config.dict()
                config_dict["logging"]["level"] = (
                    config_dict.get("logging").get("level").upper()
                )
                validate_config(config_dict)
                return config_dict, parsed_config
        except IOError as err:
            print(f"no config file found at {path}. Error : {err}")
            return conf_obj.dict(), conf_obj

    except Exception as err:
        print(f"Error while loading config details, err: {err}")
        return {}, {}
