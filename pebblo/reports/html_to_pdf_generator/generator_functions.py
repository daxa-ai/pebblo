from weasyprint import HTML, CSS
from xhtml2pdf import pisa
import os

# Creates PDF from template using weasyprint
def weasyprint_pdf_converter(sourceHtml, outputPath, searchPath):
    base_url = os.path.dirname(os.path.realpath(__file__))
    htmldoc = HTML(string=sourceHtml, base_url=base_url)
    return htmldoc.write_pdf(target=outputPath, stylesheets=[CSS(searchPath + '/index.css')])

# Creates PDF from template using xhtml2pdf
def xhtml2pdf_pdf_converter(sourceHtml, outputPath, searchPath):
    resultFile = open(outputPath, "w+b")
    pisaStatus = pisa.CreatePDF(src=sourceHtml,           
        dest=resultFile)
    resultFile.close()
    return pisaStatus.err