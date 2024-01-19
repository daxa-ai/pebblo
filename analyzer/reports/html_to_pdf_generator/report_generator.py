from weasyprint import HTML, CSS
import jinja2
import datetime
import os

# Convert HTML Template to PDF by embedding JSON data
def convertHtmlToPdf(data, outputPath, templateName, searchPath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchPath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(templateName)
    sourceHtml = template.render(data=data, date=datetime.datetime.now())
    base_url = os.path.dirname(os.path.realpath(__file__))
    htmldoc = HTML(string=sourceHtml, base_url=base_url)
    return htmldoc.write_pdf(target=outputPath, stylesheets=[CSS(searchPath + '/index.css')])
