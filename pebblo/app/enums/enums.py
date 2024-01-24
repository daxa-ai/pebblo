"""
These are all enums related to Inspector.
"""
from enum import Enum


class CacheDir(Enum):
    metadata_folder = "/metadata"
    metadata_file_path = f"{metadata_folder}/metadata.json"
    report_file_name = "report.json"
    pdf_report_file_name = "pebblo_report.pdf"
    home_dir = ".pebblo"


class ReportConstants(Enum):
    snippets_limit = 100
    top_findings_limit = 5
