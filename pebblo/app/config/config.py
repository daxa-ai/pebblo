import yaml

from pydantic import BaseSettings, Field
import pathlib

# Default config value
dir_path = pathlib.Path().absolute()

# Port BaseModel
class PortConfig(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=8000)


# Report BaseModel
class ReportConfig(BaseSettings):
    format: str = Field(default='pdf')
    renderer: str = Field(default='weasyprint')
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
        conf_obj = Config(
            daemon=PortConfig(
                host='localhost',
                port=8000
            ),
            reports=ReportConfig(
                format='pdf',
                renderer='weasyprint',
                outputDir='~/.pebblo'
            ),
            logging=LoggingConfig(
                level='info'
            )
        )
        if not path:
            # Setting Default config details
            return conf_obj.dict()

        # If Path exist, set config value
        else:
            con_file = path
            try:
                with open(con_file, "r") as output:
                    cred_json = yaml.safe_load(output)
                    parsed_config = Config.parse_obj(cred_json)
                    config_dict = parsed_config.dict()
                    return config_dict
            except IOError as err:
                print(f"no credentials file found at {con_file}")
                return conf_obj.dict()

    except Exception as err:
        print(f'Error while loading config details, err: {err}')


