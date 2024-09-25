import sys
from contextvars import ContextVar
from typing import Optional, Tuple

import yaml

from pebblo.app.config.models import (
    ClassifierConfig,
    Config,
    DaemonConfig,
    LoggingConfig,
    ReportConfig,
    StorageConfig,
)
from pebblo.app.enums.common import ClassificationMode

var_server_config: ContextVar[Config] = ContextVar("server_config", default=None)
var_server_config_dict: ContextVar[dict] = ContextVar("server_config_dict", default={})


def get_default_config_values():
    # set default config value
    conf_obj = Config(
        daemon=DaemonConfig(host="localhost", port=8000),
        reports=ReportConfig(format="pdf", renderer="xhtml2pdf", cacheDir="~/.pebblo"),
        logging=LoggingConfig(),
        classifier=ClassifierConfig(
            mode=ClassificationMode.ALL.value, anonymizeSnippets=False
        ),
        storage=StorageConfig(type="file", db=None),
        # for now, a default storage type is FILE, but in the next release DB will be the default storage type.
    )
    return conf_obj.dict(), conf_obj


def load_config(path: Optional[str]) -> Tuple[dict, Config]:
    try:
        if not path:
            # If Path does not exist in command, set default config value
            return get_default_config_values()

        # If Path exist, set config value
        try:
            with open(path, "r") as output:
                cred_yaml = yaml.safe_load(output)
                parsed_config = Config.parse_obj(cred_yaml)
                config_dict = parsed_config.dict()
                config_dict["logging"]["level"] = (
                    config_dict.get("logging").get("level").upper()
                )
                return config_dict, parsed_config
        except IOError as err:
            print(f"no config file found at {path}. Error : {err}")
            return get_default_config_values()

    except Exception as err:
        print(f"Error while loading config details, err: {err}")
        print("Exiting due to validation error...")
        sys.exit()
        return {}, {}
