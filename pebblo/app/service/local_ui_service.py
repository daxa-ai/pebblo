import json

data = {
    "name": "limit_test_csv_shreyas_app_1",
    "description": "This is test csv app.",
    "framework": {
        "name": "langchain",
        "version": "0.1.15"
    },
    "reportSummary": {
        "findings": 14,
        "findingsEntities": 6,
        "findingsTopics": 8,
        "totalFiles": 1,
        "filesWithRestrictedData": 1,
        "dataSources": 1,
        "owner": "Shreyas Damle",
        "createdAt": "2024-01-24 19:49:21.066491"
    },
    "topFindings": [
        {
            "fileName": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
            "fileOwner": "shreyasdamle",
            "sourceSize": 0,
            "findingsEntities": 6,
            "findingsTopics": 8,
            "findings": 14
        }
    ],
    "instanceDetails": {
        "type": "desktop",
        "host": "OPLPT012.local",
        "path": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/basic_retrieval",
        "runtime": "local",
        "ip": "116.74.213.232",
        "language": "python",
        "languageVersion": "3.11.7",
        "platform": "macOS-14.3-arm64-arm-64bit",
        "os": "Darwin",
        "osVersion": "Darwin Kernel Version 23.3.0: Wed Dec 20 21:33:31 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T8112",
        "createdAt": "2024-01-24 19:49:21.065505",
        "id":"1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"
    },
    "dataSources": [
        {
            "name": "CSVLoader",
            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
            "sourceType": "file",
            "sourceSize": 5755,
            "totalSnippetCount": 14,
            "displayedSnippetCount": 10,
            "findingsSummary": [
                {
                    "labelName": "Credit card number",
                    "findings": 5,
                    "findingsType": "entities",
                    "snippetCount": 5,
                    "fileCount": 1
                },
                {
                    "labelName": "Medical Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1
                },
                {
                    "labelName": "Harmful Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1
                },
                {
                    "labelName": "US SSN",
                    "findings": 1,
                    "findingsType": "entities",
                    "snippetCount": 1,
                    "fileCount": 1
                }
            ],
            "findingsDetails": [
                {
                    "labelName": "Credit card number",
                    "findings": 5,
                    "findingsType": "entities",
                    "snippetCount": 5,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: Sachin's American Express credit card number is 378282246310005.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                {
                    "labelName": "Medical Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                {
                    "labelName": "Harmful Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                {
                    "labelName": "US SSN",
                    "findings": 1,
                    "findingsType": "entities",
                    "snippetCount": 1,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: Sachin's SSN is 222-85-4836\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                }
            ]
        }
    ],
    "appList":[
        {
            "name": "limit_test_csv_shreyas_app_1",
            "lastModified": "2024-01-24 19:49:51.285922",
            "instanceDetails": {
                "type": "desktop",
                "host": "OPLPT012.local",
                "path": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/basic_retrieval",
                "runtime": "local",
                "ip": "116.74.213.232",
                "language": "python",
                "languageVersion": "3.11.7",
                "platform": "macOS-14.3-arm64-arm-64bit",
                "os": "Darwin",
                "osVersion": "Darwin Kernel Version 23.3.0: Wed Dec 20 21:33:31 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T8112",
                "createdAt": "2024-01-24 19:49:21.065505",
                "id":"1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"
            },
            "application":"AcmeMort_App",
            "topics":"24",
            "entities":"12",
            "owner":"Alex M",
            "id":"1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
            "findings":[
                 {
                    "findingType":'Topic',
                    "label":'Medical Advice',
                    "sourceFiles":'12',
                    "snippets":'24',
                    "dataSource":'S3 Directory Loader',
                },
                 {
                    "findingType":'Topic',
                    "label":'Medical Advice',
                    "sourceFiles":'12',
                    "snippets":'24',
                    "dataSource":'S3 Directory Loader',
                },
            ],
          "snippets": [
                 {
                    "labelName": "Credit card number",
                    "findings": 5,
                    "findingsType": "entities",
                    "snippetCount": 5,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: Sachin's American Express credit card number is 378282246310005.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                 {
                    "labelName": "Medical Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                {
                    "labelName": "Harmful Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
            ]
        },
        {
            "name": "Healthcare_App",
            "lastModified": "2024-01-24 19:49:51.285922",
            "instanceDetails": {
                "type": "desktop",
                "host": "OPLPT012.local",
                "path": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/basic_retrieval",
                "runtime": "local",
                "ip": "116.74.213.232",
                "language": "python",
                "languageVersion": "3.11.7",
                "platform": "macOS-14.3-arm64-arm-64bit",
                "os": "Darwin",
                "osVersion": "Darwin Kernel Version 23.3.0: Wed Dec 20 21:33:31 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T8112",
                "createdAt": "2024-01-24 19:49:21.065505",
                "id":"1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"
            },
            "application":"Healthcare_App",
            "topics":"24",
            "entities":"12",
            "owner":"Jane Cooper",
            "id":"1b9d6bcd-4b2d-9b5d-ab8dfbbd4bed",
            "findings":[
                 {
                    "findingType":'Topic',
                    "label":'Medical Advice',
                    "sourceFiles":'12',
                    "snippets":'24',
                    "dataSource":'S3 Directory Loader',
                },
                 {
                    "findingType":'Topic',
                    "label":'Medical Advice',
                    "sourceFiles":'12',
                    "snippets":'24',
                    "dataSource":'S3 Directory Loader',
                },
            ],
            "snippets": [
                 {
                    "labelName": "Credit card number",
                    "findings": 5,
                    "findingsType": "entities",
                    "snippetCount": 5,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: Sachin's American Express credit card number is 378282246310005.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: wqimonZynA\nEmail: prdFTeZPsB@aaPrs.com\nSSN: 414077406\nAddress: IPPUnpNMyuAxwjMcgLkS\nCC Expiry: 10/2028\nCredit Card Number: 5474109639252365\nCC Security Code: 535\nIPv4: 196.205.119.205\nIPv6: 8f5d:7ad3:4dab:7963:6026:6157:d6bb:b99e\nPhone: 1448428824",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                 {
                    "labelName": "Medical Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is medical critical situation. You should go and get proper treatment from expert doctor.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
                {
                    "labelName": "Harmful Advice",
                    "findings": 4,
                    "findingsType": "topics",
                    "snippetCount": 4,
                    "fileCount": 1,
                    "snippets": [
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        },
                        {
                            "snippet": "Name: This is harmful advice I am giving to you.\nEmail: None\nSSN: None\nAddress: None\nCC Expiry: None\nCredit Card Number: None\nCC Security Code: None\nIPv4: None\nIPv6: None\nPhone: None",
                            "sourcePath": "/Users/shreyasdamle/work/cloud_defense/pebblo/samples/data/sens_data.csv",
                            "fileOwner": "shreyasdamle"
                        }
                    ]
                },
            ]
        },
        {
            "instanceDetails": {},
            "application":"Hrproductivity_App",
            "topics":"00",
            "entities":"00",
            "owner":"Guy Hawkins",
            "id":"1b9d6bcd-bbfd-9b5d-ab8dfbbd4bed"
        }
    ],
     "allFindings":[
         {
             "findingType":'Topic',
             "label":'Medical Advice',
             "sourceFiles":'12',
             "snippets":'24',
             "dataSource":'S3 Directory Loader',
             "application":'Healthcare_App',
         },
         {
             "findingType":'Entity',
             "label":'PII - Social Security Number',
             "sourceFiles":'12',
             "snippets":'22',
             "dataSource":'Unstructured Markdown Loader',
             "application":'AcmeMort_App',
         },
         {
             "findingType":'Topic',
             "label":'Medical Advice',
             "sourceFiles":'12',
             "snippets":'24',
             "dataSource":'S3 Directory Loader',
             "application":'Healthcare_App',
         },
         {
             "findingType":'Topic',
             "label":'Racial Bias',
             "sourceFiles":'12',
             "snippets":'20',
             "dataSource":'PDF Loader',
             "application":'App Name_130120',
         },
         {
             "findingType":'Entity',
             "label":'PHI - MRN',
             "sourceFiles":'12',
             "snippets":'16',
             "dataSource":'S3 Directory Loader',
             "application":'Healthcare_App',
         },
         {
             "findingType":'Topic',
             "label":'Medical Advice',
             "sourceFiles":'12',
             "snippets":'24',
             "dataSource":'S3 Directory Loader',
             "application":'Healthcare_App',
         },
         {
             "findingType":'Entity',
             "label":'PII - Credit Card',
             "sourceFiles":'12',
             "snippets":'18',
             "dataSource":'S3 Directory Loader',
             "application":'AcmeMort_App',
         }

     ],
     "allFilesWithFindings" : [
         {
             "fileName":"File Name_13012024",
             "size":"1 TB",
             "owner":"Alex M",
             "topics":'12',
             "entities":"24",
             "dataSource":"S3 Directory Loader",
             "application":"Healthcare_App"
         },
          {
             "fileName":"File Name_13012024",
             "size":"1 TB",
             "owner":"Jane Cooper",
             "topics":'12',
             "entities":"24",
             "dataSource":"UnstructuredMarkdownLoader",
             "application":"Healthcare_App"
         },
          {
             "fileName":"File Name_13012024",
             "size":"145 GB",
             "owner":"Cameron Williamson",
             "topics":'12',
             "entities":"24",
             "dataSource":"S3 Directory Loader",
             "application":"Application_ Name_Lorem"
         },
          {
             "fileName":"File Name_13012024_Loremipsum",
             "size":"1 TB",
             "owner":"Leslie Alexander",
             "topics":'12',
             "entities":"24",
             "dataSource":"S3 Directory Loader",
             "application":"Healthcare_App"
         },
          {
             "fileName":"File Name_13012024",
             "size":"1 TB",
             "owner":"Alex M",
             "topics":'12',
             "entities":"24",
             "dataSource":"S3 Directory Loader",
             "application":"Healthcare_App"
         },
          {
             "fileName":"File Name_13012024_Loremipsum_yghsdj",
             "size":"1 TB",
             "owner":"Jacob Jones",
             "topics":'12',
             "entities":"24",
             "dataSource":"S3 Directory Loader",
             "application":"Healthcare_App"
         }
     ]
}



class AppLocalUI:
    def getData():
        return json.dumps(data)

    def getAppData(id:str):
         appList = data.get('appList')
         filteredData = [obj for obj in appList if(obj['id'] == id)]
         return json.dumps(filteredData[0])