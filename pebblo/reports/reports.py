# Import HTML to PDF generator function

from pebblo.reports.html_to_pdf_generator.report_generator import convertHtmlToPdf;
from pebblo.reports.enums.report_libraries import ReportLibraries, template_renderer_mapping
import os

class Reports:
    # Generate report - JSON data, output file name, template file name
    @staticmethod
    def generate_report(data, outputPath='./report.pdf', format = 'pdf', renderer = ReportLibraries.WEASYPRINT):
        if format == 'pdf':
            searchPath = os.path.join(os.path.dirname(__file__), 'templates/')
            convertHtmlToPdf(data, outputPath, templateName = template_renderer_mapping[renderer], searchPath = searchPath, renderer = renderer)
