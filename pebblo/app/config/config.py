from yaml.loader import SafeLoader
import argparse
import yaml
import os
from typing import List, Optional, Tuple, Dict
from pydantic import BaseSettings, Field
import pathlib
from contextvars import ContextVar

DEFAULT_SERVICE_CONFIG = './config_default.yaml'
dir_path = pathlib.Path().absolute()


class PortConfig(BaseSettings):
    host: str = Field(default='0.0.0.0')
    port: int = Field(default=37000)


class ReportConfig(BaseSettings):
    format: str = Field(default='pdf')
    outputDir: str = Field(dir_path)


class LoggingConfig(BaseSettings):
    level: str = Field(default='info')


class Config(BaseSettings):
    daemon:  PortConfig
    reports: ReportConfig
    logging: LoggingConfig


def load_config(path) -> Config:
    if not path:
        con_file = DEFAULT_SERVICE_CONFIG
        try:
            with open(con_file, "r") as output:
                cred_json = yaml.safe_load(output)
                print(cred_json, Config)
                parsed_config = Config.parse_obj(cred_json)
                return parsed_config.dict()

        except IOError as err:
            print(f"no credentials file found at {con_file}")
    else:
        con_file = path

        try:
            with open(con_file, "r") as output:
                cred_json = yaml.safe_load(output)
                print(cred_json, Config)
                parsed_config = Config.parse_obj(cred_json)
                config_dict = parsed_config.dict()
        except IOError as err:
            print(f"no credentials file found at {con_file}")

        if config_dict:
            try:
                with open(DEFAULT_SERVICE_CONFIG, "w") as output:
                    yaml.dump(config_dict, output)
                    print(config_dict)
                    return config_dict
            except IOError as err:
                print(f"no credentials file found at {con_file}")
