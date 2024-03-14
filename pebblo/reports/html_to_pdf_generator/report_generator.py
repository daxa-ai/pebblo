"""
Report generator and supporting functions
"""

import datetime
import time
from decimal import Decimal

import jinja2

from pebblo.reports.enums.report_libraries import library_function_mapping
from pebblo.reports.libs.logger import logger


def date_formatter(date_obj):
    """Converts date string to object and returns formatted string for date (D M Y, H:M)"""
    return date_obj.strftime("%d %B %Y , %H:%M") + " " + time.localtime().tm_zone


def get_file_size(size):
    """Returns file size in KB, MB, GB as applicable"""
    power = 2**10
    n = 0
    power_labels = {0: "Bytes", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    while size > power:
        size /= power
        n += 1
    size_num = Decimal(str(size))
    size_str = str(round(size_num, 2)) + " " + power_labels.get(n, "")
    return size_str


def convert_html_to_pdf(data, output_path, template_name, search_path, renderer):
    try:
        """Convert HTML Template to PDF by embedding JSON data"""
        template_loader = jinja2.FileSystemLoader(searchpath=search_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)
        current_date = (
            datetime.datetime.now().strftime("%B %d, %Y")
            + " "
            + time.localtime().tm_zone
        )
        source_html = template.render(
            data=data,
            date=current_date,
            datastores=data["dataSources"][0],
            findingDetails=data["dataSources"][0]["findingsDetails"],
            loadHistoryItemsToDisplay=data["loadHistory"]["history"],
            dateFormatter=date_formatter,
            getFileSize=get_file_size,
        )
        pdf_converter = library_function_mapping[renderer]
        status, result = pdf_converter(source_html, output_path, search_path)
        return status, result
    except Exception as e:
        logger.error(e)
        return False, ""
