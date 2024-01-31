# Report Generator

Report Generator contains the following operations:

1. HTML to PDF generator

## How to use

```
from reports.reports import Reports;

# Define JSON Data
appData = {
  "name": "App-Name-1",
  "framework": {
    "name": "langchain",
    "version": "0.1.10"
  },
  "description": "",
  "reportSummary": {
    "findings": "14",
    "totalFile": "10",
    "filesWithRestrictedData": "24",
    "dataSources": "1",
    "owner": "John Doe",
    "createdAt": "<date-time>"
  },
  "topFindings": [
    {
      "fileName": "",
      "count": "<int>"
    },
    {
      "fileName": "",
      "count": "<int>"
    },
    {
      "fileName": "",
      "count": "<int>"
    }
  ],
  "instanceDetails": {
    "type": "desktop",
    "host": "OPLPT012.local",
    "path": "/samples/basic_retrieval",
    "runtime": "local",
    "ip": "49.248.66.146",
    "language": "python",
    "languageVersion": "3.11.5",
    "platform": "macOS-14.2.1-arm64-arm-64bit",
    "os": "Darwin",
    "osVersion": null,
    "createdAt": "<date-time>"
  }
}

# Provide JSON data, output file name, template name (from /templates directory) and reportLibrary (xhtml2pdf or weasyprint) to the generate report # function.
# Below are the default values for outputPath and templateName:
  Reports.generate_report(data, outputPath='./report.pdf', templateName='reportTemplate.html', reportLibrary='xhtml2pdf')
```
