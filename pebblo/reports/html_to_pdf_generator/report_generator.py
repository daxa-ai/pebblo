"""
Report generator and supporting functions
"""

import datetime
import time
from decimal import Decimal

import jinja2

from pebblo.log import get_logger
from pebblo.reports.enums.keyword_mapping import topic_entity_mapping
from pebblo.reports.enums.report_libraries import library_function_mapping

logger = get_logger(__name__)


def date_formatter(date_obj, show_timezone=True):
    """Converts date string to object and returns formatted string for date (D M Y, H:M)"""
    date_str = date_obj.strftime("%d %B %Y , %H:%M")
    if show_timezone:
        return date_str + " " + time.localtime().tm_zone
    else:
        return date_str


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


def identity_comma_separated(identity_list):
    """Returns comma separated list of identities"""
    if identity_list:
        return ", ".join(identity_list)
    return "-"


def convert_html_to_pdf(data, output_path, template_name, search_path, renderer):
    """Convert HTML Template to PDF by embedding JSON data"""
    try:
        template_loader = jinja2.FileSystemLoader(searchpath=search_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        load_history_items = []
        findings_details = []
        datastores: dict = {}
        if "dataSources" in data and data["dataSources"]:
            datastores = data["dataSources"][0]
            if "findingsDetails" in datastores:
                findings_details = datastores["findingsDetails"]
        if "loadHistory" in data and "history" in data["loadHistory"]:
            load_history_items = data["loadHistory"]["history"]
        findings_count = data["reportSummary"].get("findings", 0)
        clientVersion = ""
        versionObj = data.get("clientVersion")
        if versionObj and versionObj.get("version"):
            clientVersion = " ".join(
                [versionObj.get("name", ""), versionObj.get("version", "")]
            )
        source_html = template.render(
            data=data,
            date=current_date,
            datastores=datastores,
            findingDetails=findings_details,
            loadHistoryItemsToDisplay=load_history_items,
            dateFormatter=date_formatter,
            getFileSize=get_file_size,
            findings_count=findings_count,
            identity_comma_separated=identity_comma_separated,
            topic_entity_mapping=topic_entity_mapping,
            clientVersion=clientVersion,
        )
        pdf_converter = library_function_mapping[renderer]
        status, result = pdf_converter(source_html, output_path, search_path)
        return status, result
    except Exception as e:
        logger.error(e)
        return False, ""
