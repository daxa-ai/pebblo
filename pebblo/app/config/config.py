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
        conf_obj = Config(
            daemon=PortConfig(
                host='0.0.0.0',
                port=3700
            ),
            reports=ReportConfig(
                format='pdf',
                outputDir='/home/Kunal/pebblo'
            ),
            logging=LoggingConfig(
                level='info'
            )
        )
        return conf_obj.dict()
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