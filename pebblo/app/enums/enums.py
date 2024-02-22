"""
These are all enums related to Inspector.
"""
from enum import Enum
from pebblo.app.daemon import config_details


class CacheDir(Enum):
    metadata_folder = "/metadata"
    metadata_file_path = f"{metadata_folder}/metadata.json"
    report_data_file_name = "report.json"
    report_file_name = f"pebblo_report.{config_details.get('reports', {}).get('format')}"
    home_dir = config_details.get('reports', {}).get('outputDir', '~/.pebblo')
    renderer = config_details.get('reports', {}).get('renderer')
    format = config_details.get('reports', {}).get('format')
    proxy = f"http://{config_details.get('daemon', {}).get('host')}:{config_details.get('daemon', {}).get('port')}"



class ReportConstants(Enum):
    snippets_limit = 100
    top_findings_limit = 5
    loader_history_limit = 5
