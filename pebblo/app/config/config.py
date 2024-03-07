import pathlib

import yaml
from pydantic import BaseSettings, Field

from pebblo.app.config.config_validation import validate_config

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
    outputDir: str = Field(dir_path)


# Logging BaseModel
class LoggingConfig(BaseSettings):
    level: str = Field(default="info")


class ClassifierConfig(BaseSettings):
    anonymizeAllEntities: bool = Field(default=True)


# ConfigFile BaseModel
class Config(BaseSettings):
    daemon: PortConfig
    reports: ReportConfig
    logging: LoggingConfig
    classifier: ClassifierConfig


def load_config(path) -> dict:
    try:
        # If Path does not exist in command, set default config value
        conf_obj = Config(
            daemon=PortConfig(host="localhost", port=8000),
            reports=ReportConfig(
                format="pdf", renderer="xhtml2pdf", outputDir="~/.pebblo"
            ),
            logging=LoggingConfig(level="info"),
            classifier=ClassifierConfig(anonymizeAllEntities=True),
        )
        if not path:
            # Setting Default config details
            return conf_obj.dict()

        # If Path exist, set config value
        con_file = path
        try:
            with open(con_file, "r") as output:
                cred_json = yaml.safe_load(output)
                parsed_config = Config.parse_obj(cred_json)
                config_dict = parsed_config.dict()
                validate_config(config_dict)
                return config_dict
        except IOError as err:
            print(f"no credentials file found at {con_file}. Error : {err}")
            return conf_obj.dict()

    except Exception as err:
        print(f"Error while loading config details, err: {err}")
