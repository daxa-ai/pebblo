# Import HTML to PDF generator function
from reports.html_to_pdf_generator.report_generator import convertHtmlToPdf;

class Reports:

    # Generate report - JSON data, output file name, template file name
    def generate_report(data, outputPath = './report.pdf', templateName = 'reportTemplate.html'):
        convertHtmlToPdf(data, outputPath, templateName)