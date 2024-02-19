from pebblo.reports.html_to_pdf_generator.generator_functions import weasyprint_pdf_converter, xhtml2pdf_pdf_converter

# Defines the PDF renderer libraries
class ReportLibraries:
    XHTML2PDF = "xhtml2pdf"
    WEASYPRINT = "weasyprint"


library_function_mapping = {
    ReportLibraries.XHTML2PDF: xhtml2pdf_pdf_converter,
    ReportLibraries.WEASYPRINT: weasyprint_pdf_converter
}

template_renderer_mapping = {
    ReportLibraries.XHTML2PDF: 'xhtml2pdfTemplate.html',
    ReportLibraries.WEASYPRINT: 'weasyprintTemplate.html'
}