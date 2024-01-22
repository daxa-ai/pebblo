"""
These are all enums related to Inspector.
"""
from enum import Enum


class CacheDir(Enum):
    metadata_folder = "/metadata"
    metadata_file_path = f"{metadata_folder}/metadata.json"
    report_file_name = "report.json"
    pdf_report_file_name = "pdf_report.pdf"
    home_dir = ".daxa"
