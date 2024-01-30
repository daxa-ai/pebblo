from weasyprint import HTML, CSS
import jinja2
import datetime
from decimal import Decimal
from dateutil import tz
import os

# Converts date string to object and returns formatted string for date (D M Y, H:M)
def dateFormatter(utc_date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.tzlocal()
    utc_date = utc_date.replace(tzinfo=from_zone)
    local_date = utc_date.astimezone(to_zone)
    return local_date.strftime('%d %B %Y , %H:%M')

# Returns file size in KB, MB, GB as applicable
def getFileSize(size):
    power = 2**10
    n = 0
    power_labels = {0 : 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    sizeNum = Decimal(str(size))
    sizeStr = str(round(sizeNum, 2)) + " " + power_labels.get(n, '')
    return sizeStr


# Convert HTML Template to PDF by embedding JSON data
def convertHtmlToPdf(data, outputPath, templateName, searchPath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchPath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(templateName)
    sourceHtml = template.render(data=data, date=datetime.datetime.now(), datastores=data["dataSources"][0], findingDetails=data["dataSources"][0]["findingsDetails"], dateFormatter=dateFormatter, getFileSize=getFileSize)
    base_url = os.path.dirname(os.path.realpath(__file__))
    htmldoc = HTML(string=sourceHtml, base_url=base_url)
    return htmldoc.write_pdf(target=outputPath, stylesheets=[CSS(searchPath + '/index.css')])
