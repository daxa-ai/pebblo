"""
Copyright (c) 2024 Daxa. All rights reserved.

These are all enums related to Inspector.
"""
from enum import Enum


class CacheDir(Enum):
    metadata_folder = "/metadata"
    metadata_file_path = f"{metadata_folder}/metadata.json"
    report_file_name = "report.json"
    home_dir = ".daxa"
