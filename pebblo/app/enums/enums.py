"""
These are all enums related to Pebblo Server.
"""

from enum import Enum

from pebblo.app.config.config import var_server_config_dict

config_details = var_server_config_dict.get()


class CacheDir(Enum):
    """
    Enums for cache directory
    """

    METADATA_FOLDER = "/metadata"
    METADATA_FILE_PATH = f"{METADATA_FOLDER}/metadata.json"
    APPLICATION_METADATA_FILE_PATH = f"{METADATA_FOLDER}/app_metadata.json"
    APPLICATION_METADATA_LOCK_FILE_PATH = f"{METADATA_FOLDER}/app_metadata_lock_file"
    METADATA_LOCK_FILE_PATH = f"{METADATA_FOLDER}/metadata_lock_file"
    REPORT_DATA_FILE_NAME = "report.json"
    REPORT_FILE_NAME = (
        f"pebblo_report.{config_details.get('reports', {}).get('format')}"
    )
    HOME_DIR = config_details.get("reports", {}).get("cacheDir", "~/.pebblo")
    RENDERER = config_details.get("reports", {}).get("renderer")
    FORMAT = config_details.get("reports", {}).get("format")
    PROXY = (
        f"http://{config_details.get('daemon', {}).get('host')}:"
        f"{config_details.get('daemon', {}).get('port')}"
    )
    DB_NAME = config_details.get("storage", {}).get("name")
    DB_LOCATION = config_details.get("storage", {}).get("location")

    SQLITE_ENGINE = "sqlite:///{}/pebblo.db"
    # SQLITE_ENGINE = f"sqlite:///{DB_LOCATION}/{DB_NAME}.db"


class ReportConstants(Enum):
    """
    Enums for report
    """

    SNIPPET_LIMIT = 100
    TOP_FINDINGS_LIMIT = 5
    LOADER_HISTORY__LIMIT = 5


class ClassifierConstants(Enum):
    anonymize_snippets = config_details.get("classifier", {}).get("anonymizeSnippets")


class ApplicationTypes(Enum):
    LOADER = "loader"
    RETRIEVAL = "retrieval"
