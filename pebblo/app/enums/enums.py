"""
These are all enums related to Inspector.
"""
from enum import Enum
import os
from pebblo.app.daemon import config_details


class CacheDir(Enum):
    metadata_folder = "/metadata"
    metadata_file_path = f"{metadata_folder}/metadata.json"
    report_file_name = "report.json"
    pdf_report_file_name = "pebblo_report.pdf"
    home_dir = config_details.get('reports', {}).get('outputDir', '~/.pebblo')


class ReportConstants(Enum):
    snippets_limit = 100
    top_findings_limit = 5
    loader_history_limit = 5
