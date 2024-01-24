from weasyprint import HTML, CSS
import jinja2
import datetime
import os

# Converts date string to object and returns formatted string for date (D M Y, H:M)
def dateFormatter(date_string):
    date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return date_obj.strftime('%d %B %Y , %H:%M')

# Convert HTML Template to PDF by embedding JSON data
def convertHtmlToPdf(data, outputPath, templateName, searchPath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchPath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(templateName)
    sourceHtml = template.render(data=data, date=datetime.datetime.now(), datastores=data["dataSources"][0], findingDetails=data["dataSources"][0]["findingsDetails"], dateFormatter=dateFormatter)
    base_url = os.path.dirname(os.path.realpath(__file__))
    htmldoc = HTML(string=sourceHtml, base_url=base_url)
    return htmldoc.write_pdf(target=outputPath, stylesheets=[CSS(searchPath + '/index.css')])
