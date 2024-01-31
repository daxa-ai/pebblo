# Import HTML to PDF generator function

from pebblo.reports.html_to_pdf_generator.report_generator import convertHtmlToPdf;
from pebblo.reports.enums.report_libraries import ReportLibraries
import os

class Reports:
    # Generate report - JSON data, output file name, template file name
    @staticmethod
    def generate_report(data, outputPath='./report.pdf', templateName='xhtml2pdfTemplate.html', reportLibrary = ReportLibraries.XHTML2PDF):
        searchPath = os.path.join(os.path.dirname(__file__), 'templates/')
        convertHtmlToPdf(data, outputPath, templateName = templateName, searchPath = searchPath, reportLibrary = reportLibrary)
