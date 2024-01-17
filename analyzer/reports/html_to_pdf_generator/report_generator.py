from weasyprint import HTML, CSS
import jinja2
import datetime

# Convert HTML Template to PDF by embedding JSON data
def convertHtmlToPdf(data, outputPath, templateName):
    templateLoader = jinja2.FileSystemLoader(searchpath="reports/templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(templateName)
    sourceHtml = template.render(data=data, date=datetime.datetime.now()) 
    htmldoc = HTML(string=sourceHtml, base_url="")
    return  htmldoc.write_pdf(target=outputPath, stylesheets=[CSS('reports/templates/index.css')])