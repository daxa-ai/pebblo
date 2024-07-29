import pathlib
from contextvars import ContextVar
from typing import Tuple

import yaml
from pydantic import BaseSettings, Field

from pebblo.app.config.config_validation import validate_config, validate_input

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
DEFAULT_LOG_MAX_FILE_SIZE = 2 * 1024 * 1024
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


# ConfigFile BaseModel
class Config(BaseSettings):
    daemon: PortConfig
    reports: ReportConfig
    logging: LoggingConfig
    classifier: ClassifierConfig


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
        return {}
