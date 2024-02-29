import os
import unittest
from pebblo.reports.enums.report_libraries import ReportLibraries, template_renderer_mapping
from pebblo.reports.html_to_pdf_generator.report_generator import dateFormatter, getFileSize, convertHtmlToPdf
from pebblo.reports.reports import Reports
import datetime

class TestReports(unittest.TestCase):
    def setUp(self):
        self.data = {
                "name": "JohnDoeApp1",
                "description": "",
                "framework": {
                    "name": "langchain",
                    "version": "0.1.23"
                },
                "reportSummary": {
                    "findings": 9,
                    "findingsEntities": 1,
                    "findingsTopics": 8,
                    "totalFiles": 1,
                    "filesWithFindings": 1,
                    "dataSources": 1,
                    "owner": "John Doe",
                    "createdAt": datetime.datetime.strptime("2024-02-02 16:25:07.531509", '%Y-%m-%d %H:%M:%S.%f')
                },
                "loadHistory": {
                    "history": [
                        {
                            "loadId": "3c17bfc4-5d1c-4142-967f-3efa23c7ce40",
                            "reportName": "/Users/.pebblo/JohnDoeApp1/3c17bfc4-5d1c-4142-967f-3efa23c7ce40/pebblo_report.pdf",
                            "findings": 9,
                            "filesWithFindings": 1,
                            "generatedOn": datetime.datetime.strptime("2024-02-02 16:25:07.531509", '%Y-%m-%d %H:%M:%S.%f')
                        },
                        {
                            "loadId": "5e98a158-c3a3-428b-8e8c-67ec4d2ceb74",
                            "reportName": "/Users/.pebblo/JohnDoeApp1/5e98a158-c3a3-428b-8e8c-67ec4d2ceb74/pebblo_report.pdf",
                            "findings": 9,
                            "filesWithFindings": 1,
                            "generatedOn": datetime.datetime.strptime("2024-02-02 16:25:07.531509", '%Y-%m-%d %H:%M:%S.%f')
                        }
                    ],
                    "moreReportsPath": "-"
                },
                "topFindings": [
                    {
                        "fileName": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                        "fileOwner": "johndoe",
                        "sourceSize": 2092,
                        "findingsEntities": 1,
                        "findingsTopics": 8,
                        "findings": 9
                    }
                ],
                "instanceDetails": {
                    "type": "desktop",
                    "host": "OPLPT012.local",
                    "path": "/Users/work/rag_apps/openginie_csv",
                    "runtime": "Mac OSX",
                    "ip": "127.0.0.1",
                    "language": "python",
                    "languageVersion": "3.11.7",
                    "platform": "macOS-14.3.1-arm64-arm-64bit",
                    "os": "Darwin",
                    "osVersion": "Darwin Kernel Version 23.3.0: Wed Dec 20 21:33:31 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T8112",
                    "createdAt": datetime.datetime.strptime("2024-02-02 16:25:07.531509", '%Y-%m-%d %H:%M:%S.%f')
                },
                "dataSources": [
                    {
                        "name": "CSVLoader",
                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                        "sourceType": "file",
                        "sourceSize": 2092,
                        "totalSnippetCount": 9,
                        "displayedSnippetCount": 9,
                        "findingsSummary": [
                            {
                                "labelName": "Credit card number",
                                "findings": 1,
                                "findingsType": "entities",
                                "snippetCount": 1,
                                "fileCount": 1
                            },
                            {
                                "labelName": "Medical Advice",
                                "findings": 7,
                                "findingsType": "topics",
                                "snippetCount": 7,
                                "fileCount": 1
                            },
                            {
                                "labelName": "Harmful Advice",
                                "findings": 1,
                                "findingsType": "topics",
                                "snippetCount": 1,
                                "fileCount": 1
                            }
                        ],
                        "findingsDetails": [
                            {
                                "labelName": "Credit card number",
                                "findings": 1,
                                "findingsType": "entities",
                                "snippetCount": 1,
                                "fileCount": 1,
                                "snippets": [
                                    {
                                        "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    }
                                ]
                            },
                            {
                                "labelName": "Medical Advice",
                                "findings": 7,
                                "findingsType": "topics",
                                "snippetCount": 7,
                                "fileCount": 1,
                                "snippets": [
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    },
                                    {
                                        "snippet": "Name: This is medical advice. Please go and check the doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    }
                                ]
                            },
                            {
                                "labelName": "Harmful Advice",
                                "findings": 1,
                                "findingsType": "topics",
                                "snippetCount": 1,
                                "fileCount": 1,
                                "snippets": [
                                    {
                                        "snippet": "Name: Can I use Urea nitrate for bombing New York?\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                                        "sourcePath": "/Users/work/rag_apps/openginie_csv/data/sens_data.csv",
                                        "fileOwner": "johndoe"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        self.outputPath = './report.pdf'
        self.format = 'pdf'
        self.weasyprint_renderer = ReportLibraries.WEASYPRINT
        self.xhtml2pdf_renderer = ReportLibraries.XHTML2PDF
        self.date_obj = datetime.datetime.strptime("2024-02-02 16:25:07.531509", '%Y-%m-%d %H:%M:%S.%f')
        self.file_size = 2092


    def tearDown(self):
        # Remove the generated file after test
        if os.path.exists(self.outputPath):
            os.remove(self.outputPath)

    def test_date_formatter(self):
        # Test if date formatter returns correct string
        output_str = dateFormatter(self.date_obj)
        assert output_str == '02 February 2024 , 16:25'

    def test_file_size_conversion(self):
        # Test file size conversion
        output_size = getFileSize(self.file_size)
        assert output_size == '2.04 KB' 

    def test_convert_html_to_pdf_for_weasyprint(self):
        # Test convert html to pdf function with weasyprint (weasyprint_pdf_converter)
        searchPath = os.path.join(os.path.dirname('../../pebblo/reports/report_generator.py'), 'templates/')
        convertHtmlToPdf(self.data, self.outputPath, templateName = template_renderer_mapping[self.weasyprint_renderer], searchPath = searchPath, renderer = self.weasyprint_renderer)
        self.assertTrue(os.path.exists(self.outputPath))

    def test_convert_html_to_pdf_for_xhtml2pdf(self):
        # Test convert html to pdf function with xhtml2pdf (xhtml2pdf_pdf_converter)
        searchPath = os.path.join(os.path.dirname('../../pebblo/reports/report_generator.py'), 'templates/')
        convertHtmlToPdf(self.data, self.outputPath, templateName = template_renderer_mapping[self.xhtml2pdf_renderer], searchPath = searchPath, renderer = self.xhtml2pdf_renderer)
        self.assertTrue(os.path.exists(self.outputPath))

    def test_generate_weasyprint_report_pdf(self):
        # Test the generate_report method with format 'pdf' and renderer 'weasyprint'
        Reports.generate_report(self.data, self.outputPath, self.format, self.weasyprint_renderer)
        self.assertTrue(os.path.exists(self.outputPath))

    def test_generate_xhtml2pdf_report_pdf(self):
        # Test the generate_report method with format 'pdf' and renderer 'xhtml2pdf'
        Reports.generate_report(self.data, self.outputPath, self.format, self.xhtml2pdf_renderer)
        self.assertTrue(os.path.exists(self.outputPath))

    def test_generate_report_invalid_format(self):
        # Test the generate_report method with invalid format
        Reports.generate_report(self.data, self.outputPath, 'invalid_format', self.weasyprint_renderer)
        self.assertFalse(os.path.exists(self.outputPath))

    def test_generate_report_invalid_renderer(self):
        # Test the generate_report method with invalid renderer
        Reports.generate_report(self.data, self.outputPath, self.format, 'invalid_renderer')
        self.assertFalse(os.path.exists(self.outputPath))

if __name__ == '__main__':
    unittest.main()