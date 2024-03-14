"""
These are all enums related to Pebblo Server.
"""

from enum import Enum

from pebblo.app.daemon import config_details


class CacheDir(Enum):
    """
    Enums for cache directory
    """

    METADATA_FOLDER = "/metadata"
    METADATA_FILE_PATH = f"{METADATA_FOLDER}/metadata.json"
    REPORT_DATA_FILE_NAME = "report.json"
    REPORT_FILE_NAME = (
        f"pebblo_report.{config_details.get('reports', {}).get('format')}"
    )
    HOME_DIR = config_details.get("reports", {}).get("outputDir", "~/.pebblo")
    RENDERER = config_details.get("reports", {}).get("renderer")
    FORMAT = config_details.get("reports", {}).get("format")
    PROXY = (
        f"http://{config_details.get('daemon', {}).get('host')}:"
        f"{config_details.get('daemon', {}).get('port')}"
    )


class ReportConstants(Enum):
    """
    Enums for report
    """

    SNIPPET_LIMIT = 100
    TOP_FINDINGS_LIMIT = 5
    LOADER_HISTORY__LIMIT = 5


class ClassifierConstants(Enum):
    anonymize_snippets = config_details.get("classifier", {}).get("anonymizeSnippets")
