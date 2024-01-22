# Import HTML to PDF generator function

from pebblo.reports.html_to_pdf_generator.report_generator import convertHtmlToPdf;
import os

class Reports:
    # Generate report - JSON data, output file name, template file name
    @staticmethod
    def generate_report(data, outputPath='./report.pdf', templateName='reportTemplate.html'):
        searchPath = os.path.join(os.path.dirname(__file__), 'templates/')
        convertHtmlToPdf(data, outputPath, templateName = templateName, searchPath=searchPath)
