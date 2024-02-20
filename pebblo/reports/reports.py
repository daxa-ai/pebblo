# Import HTML to PDF generator function

from pebblo.reports.html_to_pdf_generator.report_generator import convertHtmlToPdf;
from pebblo.reports.enums.report_libraries import ReportLibraries, template_renderer_mapping
from pebblo.reports.libs.logger import logger
import os

class Reports:
    # Generate report - JSON data, output file name, template file name
    @staticmethod
    def generate_report(data, outputPath='./report.pdf', format = 'pdf', renderer = ReportLibraries.WEASYPRINT):
        if format == 'pdf':
            searchPath = os.path.join(os.path.dirname(__file__), 'templates/')
            try:
                templateName = template_renderer_mapping[renderer]
                convertHtmlToPdf(data, outputPath, templateName = templateName, searchPath = searchPath, renderer = renderer)
            except Exception as e:
                logger.error(f"Renderer {renderer} not supported. Please use supported renderers: {ReportLibraries.WEASYPRINT} or {ReportLibraries.XHTML2PDF}, {e}")
        else:
            logger.error(f"Output file format {format} not supported")
