import pathlib

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


# Logging BaseModel
class LoggingConfig(BaseSettings):
    level: str = Field(default="info")


class ClassifierConfig(BaseSettings):
    anonymizeSnippets: bool = Field(default=True)


# ConfigFile BaseModel
class Config(BaseSettings):
    version: str = Field(default="unknown")
    daemon: PortConfig
    reports: ReportConfig
    logging: LoggingConfig
    classifier: ClassifierConfig


def load_config(path, version) -> dict:
    try:
        # If Path does not exist in command, set default config value
        conf_obj = Config(
            version=version,
            daemon=PortConfig(host="localhost", port=8000),
            reports=ReportConfig(
                format="pdf", renderer="xhtml2pdf", cacheDir="~/.pebblo"
            ),
            logging=LoggingConfig(level="info"),
            classifier=ClassifierConfig(anonymizeSnippets=False),
        )
        if not path:
            # Setting Default config details
            return conf_obj.dict()

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
                validate_config(config_dict)
                return config_dict
        except IOError as err:
            print(f"no config file found at {path}. Error : {err}")
            return conf_obj.dict()

    except Exception as err:
        print(f"Error while loading config details, err: {err}")
        return {}
