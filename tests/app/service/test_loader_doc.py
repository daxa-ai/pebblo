import datetime
import pytest
from unittest.mock import MagicMock, patch
from pebblo.app.models.models import Summary, DataSource
from pebblo.app.service.doc_helper import LoaderHelper, AiDataModel

data = {
    "name": "UnitTestApp",
    "owner": "AppOwner",
    "docs": [
        {
            "doc": "Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806",
            "source_path": "/home/ubuntu/sens_data.csv",
            "last_modified": datetime.datetime.now(),
            "file_owner": "FileOwner",
            "source_path_size": 1000
        }
    ],
    "plugin_version": "0.1.0",
    "load_id": "a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9",
    "loader_details": {
        "loader": "CSVLoader",
        "source_path": "/home/ubuntu/sens_data.csv",
        "source_type": "file",
        "source_path_size": 1000
    },
    "loading_end": True,
    "source_owner": "SourceOwner"
}

app_details = {
    "metadata": {
        "createdAt": "2024-01-31 13:58:35.937444",
        "modifiedAt": "2024-01-31 13:58:35.937444"
    },
    "name": "UnitTestApp",
    "description": "",
    "owner": "AppOwner",
    "pluginVersion": "0.1.0",
    "instanceDetails": {
        "type": "local",
        "host": "OPLPT058",
        "path": "/home/ubuntu/scripts",
        "runtime": "local",
        "ip": "103.197.75.199",
        "language": "python",
        "languageVersion": "3.11.7",
        "platform": "Windows-10-10.0.19045-SP0",
        "os": "Windows",
        "osVersion": "10.0.19045",
        "createdAt": "2024-01-31 13:58:05.402976"
    },
    "framework": {
        "name": "langchain",
        "version": "0.1.16"
    },
    "lastUsed": "2024-01-31 13:58:35.937444"
}

raw_data = {"total_findings": 0, "findings_entities": 0, "findings_topics": 0,
            "data_source_count": 1, "data_source_snippets": list(),
            "loader_source_snippets": {}, "file_count": 0,
            "snippet_count": 0, "data_source_findings": {},
            "snippet_counter": 0, "total_snippet_counter": 0}


@pytest.fixture
def loader_helper():
    return LoaderHelper(app_details, data=data, load_id=data.get("load_id"))


@pytest.fixture
def mock_read_json_file():
    with patch('pebblo.app.service.service.read_json_file') as mock_read_json_file:
        yield mock_read_json_file


def test_get_doc_report_metadata(loader_helper):
    # Define static input
    doc = {"doc": "sample doc", "entities": {"Credit card number": 1, "aws access key": 1}, "entityCount": 2,
           "topicCount": 1,
           "topics": {"Medical Advice": 1}, "fileOwner": "fileOwner", "sourceSize": 1000,
           "sourcePath": "/home/ubuntu/sens_data.csv"}

    output = loader_helper._get_doc_report_metadata(doc, raw_data)
    expected_output = {
        'total_findings': 3,
        'findings_entities': 2,
        'findings_topics': 1,
        'data_source_count': 1,
        'data_source_snippets': [

        ],
        'loader_source_snippets': {
            '/home/ubuntu/sens_data.csv': {
                'findings_entities': 2,
                'findings_topics': 1,
                'findings': 3,
                'fileOwner': 'fileOwner',
                'sourceSize': 1000
            }
        },
        'file_count': 1,
        'snippet_count': 1,
        'data_source_findings': {
            'Medical Advice': {
                'labelName': 'Medical Advice',
                'findings': 1,
                'findingsType': 'topics',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'sample doc',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            },
            'Credit card number': {
                'labelName': 'Credit card number',
                'findings': 1,
                'findingsType': 'entities',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'sample doc',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            },
            'aws access key': {
                'labelName': 'aws access key',
                'findings': 1,
                'findingsType': 'entities',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'sample doc',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            }
        },
        'snippet_counter': 3,
        'total_snippet_counter': 3
    }
    assert output == expected_output


def test_get_classifier_response(loader_helper):
    # Define static input
    doc = data.get('docs')[0]

    # Mock classifier responses
    mock_topic_classifier_response = {"Medical Advice": 1}, 1
    mock_entity_classifier_response = {"Credit card number": 1}, 1
    mock_secret_classifier_response = {"aws access key": 1}, 1

    # Mock classifier methods
    loader_helper.topic_classifier_obj.predict = MagicMock(return_value=mock_topic_classifier_response)
    loader_helper.entity_classifier_obj.presidio_entity_classifier = MagicMock(
        return_value=mock_entity_classifier_response)
    loader_helper.entity_classifier_obj.presidio_secret_classifier = MagicMock(
        return_value=mock_secret_classifier_response)

    # Call the method under test
    output = loader_helper._get_classifier_response(doc)

    # Expected Output
    expected_output = {
        'data': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: '
                '12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: '
                '652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
        'entityCount': 2,
        'entities': {
            'Credit card number': 1,
            'aws access key': 1
        },
        'topicCount': 1,
        'topics': {
            'Medical Advice': 1
        }
    }
    # Assertions
    assert output == expected_output


# Skipping the test because datetime.now() is not being successfully mocked.
# def test_create_doc_model(loader_helper, monkeypatch):
#     # loader_helper._create_doc_model.last_used = MagicMock(return_value=None)
#     doc = data.get('docs')[0]
#     doc_info = AiDataModel(data=doc.get('data'), entities={"Credit card number": 1, "aws access key": 1},
#                            entityCount=2, topics={"Medical Advice": 1}, topicCount=1)
#
#     # Define a custom datetime object
#
#     # Mock datetime.now() to return the custom datetime object
#     # monkeypatch.setattr(loader_helper._create_doc_model, "last_used", custom_datetime)
#
#     output = loader_helper._create_doc_model(doc, doc_info)
#     print(f"CreateDocModelOutput: {output}")
#     expected_output = {
#         'doc': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
#         'sourceSize': 1000,
#         'fileOwner': 'FileOwner',
#         'sourcePath': '/home/ubuntu/sens_data.csv',
#         'loaderSourcePath': '/home/ubuntu/sens_data.csv',
#         'lastModified': datetime.datetime(2024, 2, 6, 12, 15, 22, 271931),
#         'entityCount': 2,
#         'entities': {
#             'Credit card number': 1,
#             'aws access key': 1
#         },
#         'topicCount': 1,
#         'topics': {
#             'Medical Advice': 1
#         }
#     }
#     assert output == expected_output


def test_get_finding_details(loader_helper):
    # Define static input
    doc = {"doc": "Sample Doc", "sourcePath": "/home/ubuntu/sens_data.csv", "fileOwner": "fileOwner",
           "entities": {"Credit card number": 1, "aws access key": 1}, "entityCount": 2, "topicCount": 1,
           "topics": {"Medical Advice": 1}}
    raw_data = {"snippet_counter": 2, "total_snippet_counter": 2}
    data_source_findings = {}
    file_count = 0
    loader_helper._get_finding_details(doc, data_source_findings, "entities", file_count, raw_data)
    loader_helper._get_finding_details(doc, data_source_findings, "topics", file_count, raw_data)

    expected_raw_data = {'snippet_counter': 5, 'total_snippet_counter': 5}
    expected_data_source_findings = {
        'Credit card number': {
            'labelName': 'Credit card number',
            'findings': 1,
            'findingsType': 'entities',
            'snippetCount': 1,
            'fileCount': 0,
            'unique_snippets': {
                '/home/ubuntu/sens_data.csv'
            },
            'snippets': [
                {
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        },
        'aws access key': {
            'labelName': 'aws access key',
            'findings': 1,
            'findingsType': 'entities',
            'snippetCount': 1,
            'fileCount': 0,
            'unique_snippets': {
                '/home/ubuntu/sens_data.csv'
            },
            'snippets': [
                {
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        },
        'Medical Advice': {
            'labelName': 'Medical Advice',
            'findings': 1,
            'findingsType': 'topics',
            'snippetCount': 1,
            'fileCount': 0,
            'unique_snippets': {
                '/home/ubuntu/sens_data.csv'
            },
            'snippets': [
                {
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        }
    }

    assert raw_data == expected_raw_data
    assert data_source_findings == expected_data_source_findings


def test_update_app_details(loader_helper):
    input_data = {"loader_source_snippets": {
        '/home/ubuntu/sens_data.csv': {
            'findings_entities': 2,
            'findings_topics': 1,
            'findings': 3,
            'fileOwner': 'fileOwner',
            'sourceSize': 1000
        }
    }}
    loader_helper.app_details["loaders"] = [{
        "name": 'CSVLoader',
        "sourcePath": 'sourcePath',
        "sourceType": 'sourceType',
        "sourceSize": 1000
    }]
    ai_apps_doc = []
    loader_helper._update_app_details(input_data, ai_apps_doc)
    expected_output = {
        'metadata': {
            'createdAt': '2024-01-31 13:58:35.937444',
            'modifiedAt': '2024-01-31 13:58:35.937444'
        },
        'name': 'UnitTestApp',
        'description': '',
        'owner': 'AppOwner',
        'pluginVersion': '0.1.0',
        'instanceDetails': {
            'type': 'local',
            'host': 'OPLPT058',
            'path': '/home/ubuntu/scripts',
            'runtime': 'local',
            'ip': '103.197.75.199',
            'language': 'python',
            'languageVersion': '3.11.7',
            'platform': 'Windows-10-10.0.19045-SP0',
            'os': 'Windows',
            'osVersion': '10.0.19045',
            'createdAt': '2024-01-31 13:58:05.402976'
        },
        'framework': {
            'name': 'langchain',
            'version': '0.1.16'
        },
        'lastUsed': '2024-01-31 13:58:35.937444',
        'loaders': [
            {
                'name': 'CSVLoader',
                'sourcePath': 'sourcePath',
                'sourceType': 'sourceType',
                'sourceSize': 1000,
                'sourceFiles': [
                    {
                        'name': '/home/ubuntu/sens_data.csv',
                        'findings_entities': 2,
                        'findings_topics': 1,
                        'findings': 3
                    }
                ]
            }
        ],
        'docs': [

        ]
    }

    assert expected_output == loader_helper.app_details


def test_count_files_with_findings(loader_helper):
    loader_helper.app_details = {"loaders": [
        {"sourceFiles": [{"findings": 2}]},
        {"sourceFiles": [{"findings": 1}]},
        {"sourceFiles": [{"findings": 0}]}
    ]}

    output = loader_helper._count_files_with_findings()
    assert output == 2


# Skipping the test because datetime.now() is not being successfully mocked.
# def test_create_report_summary(loader_helper, monkeypatch):
#     input_data = {
#         'total_findings': 3,
#         'findings_entities': 2,
#         'findings_topics': 1,
#         'file_count': 1,
#         'data_source_count': 1,
#         'data_source_snippets': []
#     }
#
#     files_with_findings_count = 4
#     fixed_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
#     monkeypatch.setattr('datetime.datetime', lambda: fixed_time)
#     output = loader_helper._create_report_summary(input_data, files_with_findings_count)
#     print(f"Output: {output}")
#     assert output.dict() == {
#         'findings': 3,
#         'findingsEntities': 2,
#         'findingsTopics': 1,
#         'totalFiles': 1,
#         'filesWithFindings': 4,
#         'dataSources': 1,
#         'owner': 'pytest',
#         'createdAt': fixed_time
#     }


def test_get_top_n_findings(loader_helper):
    input_data = {"loader_source_snippets": {
        '/home/ubuntu/sens_data.csv': {
            'findings_entities': 2,
            'findings_topics': 1,
            'findings': 3,
            'fileOwner': 'fileOwner',
            'sourceSize': 1000
        }
    }}
    output = loader_helper._get_top_n_findings(input_data)
    assert len(output) == 1
    assert output == [
        {
            'fileName': '/home/ubuntu/sens_data.csv',
            'fileOwner': 'fileOwner',
            'sourceSize': 1000,
            'findingsEntities': 2,
            'findingsTopics': 1,
            'findings': 3
        }
    ]


def test_get_datasource_details(loader_helper):
    input_data = {
        'data_source_findings': {
            'Medical Advice': {
                'labelName': 'Medical Advice',
                'findings': 1,
                'findingsType': 'topics',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOnwer'
                    }
                ]
            },
            'Credit card number': {
                'labelName': 'Credit card number',
                'findings': 1,
                'findingsType': 'entities',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            },
            'aws access key': {
                'labelName': 'aws access key',
                'findings': 1,
                'findingsType': 'entities',
                'snippetCount': 1,
                'fileCount': 1,
                'unique_snippets': {
                    '/home/ubuntu/sens_data.csv'
                },
                'snippets': [
                    {
                        'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            }
        },
        'snippet_counter': 3,
        'total_snippet_counter': 3
    }
    loader_helper.app_details["loaders"] = [{
        "name": 'CSVloader',
        "sourcePath": 'sourcePath',
        "sourceType": 'sourceType',
        "sourceSize": 1000
    }]

    # Mock classifier methods
    loader_helper._create_data_source_findings_summary = MagicMock(return_value=[])
    output = loader_helper._get_data_source_details(input_data)
    expected_output = [
        DataSource(name='CSVloader',
                   sourcePath='sourcePath',
                   sourceType='sourceType',
                   sourceSize=1000,
                   totalSnippetCount=3,
                   displayedSnippetCount=3,
                   findingsSummary=[

                   ],
                   findingsDetails=[
                       {
                           'labelName': 'Medical Advice',
                           'findings': 1,
                           'findingsType': 'topics',
                           'snippetCount': 1,
                           'fileCount': 1,
                           'snippets': [
                               {
                                   'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                                   'sourcePath': '/home/ubuntu/sens_data.csv',
                                   'fileOwner': 'fileOnwer'
                               }
                           ]
                       },
                       {
                           'labelName': 'Credit card number',
                           'findings': 1,
                           'findingsType': 'entities',
                           'snippetCount': 1,
                           'fileCount': 1,
                           'snippets': [
                               {
                                   'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                                   'sourcePath': '/home/ubuntu/sens_data.csv',
                                   'fileOwner': 'fileOwner'
                               }
                           ]
                       },
                       {
                           'labelName': 'aws access key',
                           'findings': 1,
                           'findingsType': 'entities',
                           'snippetCount': 1,
                           'fileCount': 1,
                           'snippets': [
                               {
                                   'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                                   'sourcePath': '/home/ubuntu/sens_data.csv',
                                   'fileOwner': 'fileOwner'
                               }
                           ]
                       }
                   ])
    ]
    assert output == expected_output


def test_create_data_source_findings_summary(loader_helper):
    input_data = [
        {
            'labelName': 'Medical Advice',
            'findings': 1,
            'findingsType': 'topics',
            'snippetCount': 1,
            'fileCount': 1,
            'snippets': [
                {
                    'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        },
        {
            'labelName': 'Credit card number',
            'findings': 1,
            'findingsType': 'entities',
            'snippetCount': 1,
            'fileCount': 1,
            'snippets': [
                {
                    'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        },
        {
            'labelName': 'aws access key',
            'findings': 1,
            'findingsType': 'entities',
            'snippetCount': 1,
            'fileCount': 1,
            'snippets': [
                {
                    'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'fileOwner'
                }
            ]
        }
    ]

    output = loader_helper._create_data_source_findings_summary(input_data)
    expected_output = [
        {'labelName': 'Medical Advice', 'findings': 1, 'findingsType': 'topics', 'snippetCount': 1, 'fileCount': 1},
        {'labelName': 'Credit card number', 'findings': 1, 'findingsType': 'entities', 'snippetCount': 1,
         'fileCount': 1},
        {'labelName': 'aws access key', 'findings': 1, 'findingsType': 'entities', 'snippetCount': 1, 'fileCount': 1}]
    assert output == expected_output

# read json file function is not getting mocked.
# def test_get_load_history(loader_helper, mock_read_json_file):
#     loader_helper.load_id = 2
#     mock_read_json_file.return_value = {"load_ids": [1, 2, 3],
#                                         "reportSummary": {"findings": 10, "filesWithFindings": 9,
#                                                           "createdAt": datetime.datetime(2024, 1, 31, 13, 58, 5, 402976)
#                                                           }}
#
#     output = loader_helper._get_load_history()
#     print(f"LoaderHistory: {output}")
#
#     assert output == "Hello"

# Skipping the test because datetime.now() is not being successfully mocked.
# def test_generate_final_report(loader_helper):
#     # Mock Methods
#     fixed_time = datetime.datetime.now()
#     loader_helper._count_files_with_findings = MagicMock(return_value=10)
#     loader_helper._create_report_summary = MagicMock(return_value=Summary(findings=3,
#                                                                           findingsEntities=2,
#                                                                           findingsTopics=1,
#                                                                           totalFiles=1,
#                                                                           filesWithFindings=4,
#                                                                           dataSources=1,
#                                                                           owner="fileOwner",
#                                                                           createdAt=fixed_time))
#     loader_helper._get_top_n_findings = MagicMock(return_value=[
#         {
#             'fileName': '/home/ubuntu/sens_data.csv',
#             'fileOwner': 'fileOwner',
#             'sourceSize': 1000,
#             'findingsEntities': 2,
#             'findingsTopics': 1,
#             'findings': 3
#         }
#     ])
#     loader_helper._get_data_source_details = MagicMock(return_value=[DataSource(name='CSVloader',
#                                                                                 sourcePath='sourcePath',
#                                                                                 sourceType='sourceType',
#                                                                                 sourceSize=1000,
#                                                                                 totalSnippetCount=3,
#                                                                                 displayedSnippetCount=3,
#                                                                                 findingsSummary=[],
#                                                                                 findingsDetails=[])])
#
#     loader_helper._get_load_history = MagicMock(return_value=[])
#
#     output = loader_helper._generate_final_report(raw_data={})
#
#     expected_output = {
#         'name': 'UnitTestApp',
#         'description': '',
#         'framework': {
#             'name': 'langchain',
#             'version': '0.1.16'
#         },
#         'reportSummary': {
#             'findings': 3,
#             'findingsEntities': 2,
#             'findingsTopics': 1,
#             'totalFiles': 1,
#             'filesWithFindings': 4,
#             'dataSources': 1,
#             'owner': 'fileOwner',
#             'createdAt': datetime.datetime(2024, 2, 6, 12, 59, 45, 351701)
#         },
#         'loadHistory': [
#
#         ],
#         'topFindings': [
#             {
#                 'fileName': '/home/ubuntu/sens_data.csv',
#                 'fileOwner': 'fileOwner',
#                 'sourceSize': 1000,
#                 'findingsEntities': 2,
#                 'findingsTopics': 1,
#                 'findings': 3
#             }
#         ],
#         'instanceDetails': {
#             'type': 'local',
#             'host': 'OPLPT058',
#             'path': '/home/ubuntu/scripts',
#             'runtime': 'local',
#             'ip': '103.197.75.199',
#             'language': 'python',
#             'languageVersion': '3.11.7',
#             'platform': 'Windows-10-10.0.19045-SP0',
#             'os': 'Windows',
#             'osVersion': '10.0.19045',
#             'createdAt': datetime.datetime(2024, 1, 31, 13, 58, 5, 402976)
#         },
#         'dataSources': [
#             {
#                 'name': 'CSVloader',
#                 'sourcePath': 'sourcePath',
#                 'sourceType': 'sourceType',
#                 'sourceSize': 1000,
#                 'totalSnippetCount': 3,
#                 'displayedSnippetCount': 3,
#                 'findingsSummary': [
#
#                 ],
#                 'findingsDetails': [
#
#                 ]
#             }
#         ],
#         'lastModified': datetime.datetime(2024, 2, 6, 12, 59, 45, 353700)
#     }
#
#     assert output == expected_output
