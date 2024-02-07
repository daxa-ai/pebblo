import yaml

from pydantic import BaseSettings, Field
import pathlib

# Default config value
DEFAULT_SERVICE_CONFIG = './config_default.yaml'
dir_path = pathlib.Path().absolute()


# Port BaseModel
class PortConfig(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=37000)


# Report BaseModel
class ReportConfig(BaseSettings):
    format: str = Field(default='pdf')
    outputDir: str = Field(dir_path)


# Logging BaseModel
class LoggingConfig(BaseSettings):
    level: str = Field(default='info')


# ConfigFile BaseModel
class Config(BaseSettings):
    daemon:  PortConfig
    reports: ReportConfig
    logging: LoggingConfig


def load_config(path) -> Config:
    try:
        # If Path does not exist in command, set default config value
        if not path:
            # Setting Default config details
            conf_obj = Config(
                daemon=PortConfig(
                    host='0.0.0.0',
                    port=3700
                ),
                reports=ReportConfig(
                    format='pdf',
                    outputDir='./config.py'
                ),
                logging=LoggingConfig(
                    level='info'
                )
            )
            return conf_obj.dict()

        # If Path exist, set config value
        else:
            con_file = path
            try:
                with open(con_file, "r") as output:
                    cred_json = yaml.safe_load(output)
                    print(cred_json, Config)
                    parsed_config = Config.parse_obj(cred_json)
                    config_dict = parsed_config.dict()
                    return config_dict
            except IOError as err:
                print(f"no credentials file found at {con_file}")

    except Exception as err:
        print(f'Error while loading config details, err: {err}')


