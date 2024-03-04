"""
Report generator and supporting functions
"""

from decimal import Decimal
import datetime
import jinja2
from pebblo.reports.enums.report_libraries import library_function_mapping


def date_formatter(date_obj):
    """Converts date string to object and returns formatted string for date (D M Y, H:M)"""
    return date_obj.strftime("%d %B %Y , %H:%M")


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
    """Convert HTML Template to PDF by embedding JSON data"""
    template_loader = jinja2.FileSystemLoader(searchpath=search_path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    source_html = template.render(
        data=data,
        date=datetime.datetime.now(),
        datastores=data["dataSources"][0],
        findingDetails=data["dataSources"][0]["findingsDetails"],
        loadHistoryItemsToDisplay=data["loadHistory"]["history"],
        dateFormatter=date_formatter,
        getFileSize=get_file_size,
    )
    pdf_converter = library_function_mapping[renderer]
    pdf_converter(source_html, output_path, search_path)
