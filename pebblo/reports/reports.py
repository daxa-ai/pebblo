"""
Reports Module
Contains generate_report() to generate report pdf
"""
# Import HTML to PDF generator function

import os

from pebblo.log import get_logger
from pebblo.reports.enums.report_libraries import (
    ReportLibraries,
    template_renderer_mapping,
)
from pebblo.reports.html_to_pdf_generator.report_generator import convert_html_to_pdf

logger = get_logger(__name__)


class Reports:
    """
    Reports Class
    Contains generate_report() to generate report pdf
    """

    @staticmethod
    def generate_report(
        data,
        output_path="./report.pdf",
        format_string="pdf",
        renderer=ReportLibraries.XHTML2PDF,
    ):
        """Generates report pdf for given format and renderer"""
        if format_string == "pdf":
            search_path = os.path.join(os.path.dirname(__file__), "templates/")
            try:
                template_name = template_renderer_mapping[renderer]
                status, result = convert_html_to_pdf(
                    data,
                    output_path,
                    template_name=template_name,
                    search_path=search_path,
                    renderer=renderer,
                )
                return status, result

            except KeyError as e:
                logger.error(
                    "Renderer %s not supported. Please use supported renderers: "
                    "%s or %s, %s",
                    renderer,
                    ReportLibraries.WEASYPRINT,
                    ReportLibraries.XHTML2PDF,
                    e,
                )
                return False, ""
        else:
            logger.error("Output file format %s not supported", format_string)
            return False, ""
