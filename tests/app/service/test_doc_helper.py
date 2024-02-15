import datetime
import pytest
from uuid import UUID
from unittest.mock import MagicMock, patch
from pebblo.app.models.models import Summary, DataSource
from pebblo.app.service.doc_helper import LoaderHelper, AiDataModel

# static, datetime.now()
mocked_datetime = datetime.datetime(2024, 1, 1, 0, 0, 5)

data = {
    "name": "UnitTestApp",
    "owner": "pytest",
    "docs": [
        {
            "doc": "Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC "
                   "Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: "
                   "147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806",
            "source_path": "/home/ubuntu/sens_data.csv",
            "last_modified": mocked_datetime,
            "file_owner": "pytest_file_owner",
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
    "source_owner": "pytest_source_owner"
}

app_details = {
    "metadata": {
        "createdAt": mocked_datetime,
        "modifiedAt": mocked_datetime
    },
    "name": "UnitTestApp",
    "description": "",
    "owner": "pytest",
    "pluginVersion": "0.1.0",
    "instanceDetails": {
        "type": "local",
        "host": "OPLPT058",
        "path": "/home/ubuntu/scripts",
        "runtime": "local",
        "ip": "103.197.75.199",
        "language": "python",
        "languageVersion": "3.11.7",
        "platform": "mac-os",
        "os": "mac",
        "osVersion": "10.14.6",
        "createdAt": mocked_datetime
    },
    "framework": {
        "name": "langchain",
        "version": "0.1.16"
    },
    "lastUsed": mocked_datetime
}

raw_data = {"total_findings": 0, "findings_entities": 0, "findings_topics": 0,
            "data_source_count": 1, "loader_source_snippets": {}, "file_count": 0,
            "snippet_count": 0, "data_source_findings": {},
            "snippet_counter": 0, "total_snippet_counter": 0}


@pytest.fixture
def loader_helper():
    return LoaderHelper(app_details, data=data, load_id=data.get("load_id"))


@pytest.fixture
def mock_read_json_file_obj():
    with patch('pebblo.app.service.doc_helper.read_json_file') as mock_read_json_file:
        yield mock_read_json_file


@pytest.fixture
def mock_get_full_path_obj():
    with patch('pebblo.app.service.doc_helper.get_full_path') as mock_get_full_path:
        yield mock_get_full_path


@pytest.fixture
def mock_topic_classifier_obj():
    with patch('pebblo.app.service.doc_helper.topic_classifier_obj') as mock_topic_classifier:
        yield mock_topic_classifier


@pytest.fixture
def load_history_obj():
    with patch.object(LoaderHelper, '_get_load_history', return_value={
        'history': [
            {
                'loadId': UUID('a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9'),
                'reportName': '/usr/pytest-user/.pebblo/UnitTestApp/a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9'
                              '/pebblo_report.pdf',
                'findings': 10,
                'filesWithFindings': 9,
                'generatedOn': mocked_datetime
            }
        ],
        'moreReportsPath': '-'
    }) as load_history:
        yield load_history


# Test Case: 1
def test_create_doc_model(loader_helper):
    doc = data.get('docs')[0]
    doc_info = AiDataModel(data=doc.get('data'), entities={"Credit card number": 1, "aws access key": 1},
                           entityCount=2, topics={"Medical Advice": 1}, topicCount=1)
    loader_helper._get_current_datetime = MagicMock(return_value=mocked_datetime)
    output = loader_helper._create_doc_model(doc, doc_info)
    assert output["doc"] == ("Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: "
                             "ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC "
                             "Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: "
                             "8fe:d64d\nPhone: 3542039806")
    assert output["sourceSize"] == 1000
    assert output["fileOwner"] == "pytest_file_owner"
    assert output["sourcePath"] == "/home/ubuntu/sens_data.csv"
    assert output["loaderSourcePath"] == "/home/ubuntu/sens_data.csv"
    assert output["lastModified"] == mocked_datetime
    assert output["entityCount"] == 2
    assert output["entities"] == {'Credit card number': 1, 'aws access key': 1}
    assert output["topicCount"] == 1
    assert output["topics"] == {'Medical Advice': 1}


# TestCase: 2
def test_get_top_n_findings(loader_helper):
    input_data = {"loader_source_snippets": {
        '/home/ubuntu/sens_data.csv': {
            'findings_entities': 2,
            'findings_topics': 1,
            'findings': 3,
            'fileOwner': 'fileOwner',
            'sourceSize': 1000
        },
        '/home/ubuntu/sens_data_2.csv': {
            'findings_entities': 2,
            'findings_topics': 3,
            'findings': 5,
            'fileOwner': 'fileOwner2',
            'sourceSize': 1001
        }
    }}
    output = loader_helper._get_top_n_findings(input_data)
    assert len(output) == 2
    assert output == [
        {
            'fileName': '/home/ubuntu/sens_data_2.csv',
            'fileOwner': 'fileOwner2',
            'sourceSize': 1001,
            'findingsEntities': 2,
            'findingsTopics': 3,
            'findings': 5
        },
        {
            'fileName': '/home/ubuntu/sens_data.csv',
            'fileOwner': 'fileOwner',
            'sourceSize': 1000,
            'findingsEntities': 2,
            'findingsTopics': 1,
            'findings': 3
        }
    ]


# TestCase: 3
def test_count_files_with_findings(loader_helper):
    loader_helper.app_details = {"loaders": [
        {"sourceFiles": [{"findings": 2}]},
        {"sourceFiles": [{"findings": 1}]},
        {"sourceFiles": [{"findings": 0}]}
    ]}

    output = loader_helper._count_files_with_findings()
    assert output == 2


# TestCase: 4
def test_get_classifier_response(loader_helper, mock_topic_classifier_obj):
    # Define static input
    doc = data.get('docs')[0]

    # Mock classifier responses
    mock_topic_classifier_response = {"Medical Advice": 1}, 1
    mock_entity_classifier_response = {"Credit card number": 1}, 1
    mock_secret_classifier_response = {"aws access key": 1}, 1

    # Mock classifier methods
    mock_topic_classifier_obj.predict = MagicMock(return_value=mock_topic_classifier_response)
    loader_helper.entity_classifier_obj.presidio_entity_classifier = MagicMock(
        return_value=mock_entity_classifier_response)
    loader_helper.entity_classifier_obj.presidio_secret_classifier = MagicMock(
        return_value=mock_secret_classifier_response)

    # Call the method under test
    output = loader_helper._get_classifier_response(doc)
    output = output.dict()
    assert output["entityCount"] == 2
    assert output["entities"] == {
        'Credit card number': 1,
        'aws access key': 1
    }
    assert output["topicCount"] == 1
    assert output["topics"] == {
        'Medical Advice': 1
    }


# TestCase: 5
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
    assert app_details["loaders"] == [
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
    ]
    assert app_details["report_metadata"] == input_data


# TestCase: 6
def test_get_finding_details(loader_helper):
    # Define static input
    doc = {"doc": "Sample Doc", "sourcePath": "/home/ubuntu/sens_data.csv", "fileOwner": "pytest_file_owner",
           "entities": {"Credit card number": 1, "aws access key": 1}, "entityCount": 2, "topicCount": 1,
           "topics": {"Medical Advice": 1}}
    input_data = {"snippet_counter": 2, "total_snippet_counter": 2}
    data_source_findings = {}
    loader_helper._get_finding_details(doc, data_source_findings, "entities", input_data)
    loader_helper._get_finding_details(doc, data_source_findings, "topics", input_data)

    expected_data_source_findings = {
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
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'pytest_file_owner'
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
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'pytest_file_owner'
                }
            ]
        },
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
                    'snippet': 'Sample Doc',
                    'sourcePath': '/home/ubuntu/sens_data.csv',
                    'fileOwner': 'pytest_file_owner'
                }
            ]
        }
    }
    assert input_data["snippet_counter"] == 5
    assert input_data["snippet_counter"] == 5
    assert data_source_findings == expected_data_source_findings


# TestCase: 7
def test_get_data_source_details(loader_helper):
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
                        'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: '
                                   'ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: '
                                   '8048428351930771\nCC Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: '
                                   '652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: 3542039806',
                        'sourcePath': '/home/ubuntu/sens_data.csv',
                        'fileOwner': 'fileOwner'
                    }
                ]
            }
        },
        'snippet_counter': 1,
        'total_snippet_counter': 1
    }
    loader_helper.app_details["loaders"] = [{
        "name": 'CSVloader',
        "sourcePath": '/home/ubuntu/sens_data.csv',
        "sourceType": 'file',
        "sourceSize": 1000
    }]

    # Mock classifier methods
    loader_helper._create_data_source_findings_summary = MagicMock(return_value=[])
    output = loader_helper._get_data_source_details(input_data)
    expected_output = [
        DataSource(name='CSVloader',
                   sourcePath='/home/ubuntu/sens_data.csv',
                   sourceType='file',
                   sourceSize=1000,
                   totalSnippetCount=1,
                   displayedSnippetCount=1,
                   findingsSummary=[],
                   findingsDetails=[
                       {
                           'labelName': 'Medical Advice',
                           'findings': 1,
                           'findingsType': 'topics',
                           'snippetCount': 1,
                           'fileCount': 1,
                           'snippets': [
                               {
                                   'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: '
                                              '807325214\nAddress: ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit '
                                              'Card Number: 8048428351930771\nCC Security Code: 644\nIPv4: '
                                              '147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: 8fe:d64d\nPhone: '
                                              '3542039806',
                                   'sourcePath': '/home/ubuntu/sens_data.csv',
                                   'fileOwner': 'fileOwner'
                               }
                           ]
                       }
                   ])
    ]
    assert output == expected_output


# TestCase: 8
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
                    'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: '
                               'ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC '
                               'Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: '
                               '8fe:d64d\nPhone: 3542039806',
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
                    'snippet': 'Name: YqDvXJuxpH\nEmail: bTDyzanhcB@ujxtd.com\nSSN: 807325214\nAddress: '
                               'ABUbusMLXRygxzpdPOyL\nCC Expiry: 12/2030\nCredit Card Number: 8048428351930771\nCC '
                               'Security Code: 644\nIPv4: 147.17.4.121\nIPv6: 58fc: 652d:bf33:a1ab: 1f1b: 4d7d: '
                               '8fe:d64d\nPhone: 3542039806',
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
         'fileCount': 1}
    ]
    assert output == expected_output


# TestCase: 9
def test_create_report_summary(loader_helper):
    input_data = {
        'total_findings': 3,
        'findings_entities': 2,
        'findings_topics': 1,
        'file_count': 1,
        'data_source_count': 1,
        'data_source_snippets': []
    }

    files_with_findings_count = 1
    loader_helper._get_current_datetime = MagicMock(return_value=mocked_datetime)
    output = loader_helper._create_report_summary(input_data, files_with_findings_count)
    output = output.dict()
    assert output["findings"] == 3
    assert output["findingsEntities"] == 2
    assert output["findingsTopics"] == 1
    assert output["totalFiles"] == 1
    assert output["filesWithFindings"] == 1
    assert output["dataSources"] == 1
    assert output["owner"] == "pytest"
    assert output["createdAt"] == mocked_datetime


# TestCase: 10
def test_get_load_history(loader_helper, monkeypatch, mock_read_json_file_obj, mock_get_full_path_obj):
    monkeypatch.setattr("os.path.exists", lambda path: True)
    loader_helper.load_id = 2
    mock_get_full_path_response = ("/usr/pytest-user/.pebblo/UnitTestApp/a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9"
                                   "/pebblo_report.pdf")
    mock_read_json_file_obj.return_value = {"load_ids": ["a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9"],
                                            "reportSummary": {"findings": 10, "filesWithFindings": 9,
                                                              "createdAt": mocked_datetime
                                                              }}
    mock_get_full_path_obj.return_value = mock_get_full_path_response

    output = loader_helper._get_load_history()

    assert output == {
        'history': [
            {
                'loadId': UUID('a4f79ee7-42a7-48b5-9ab2-f7a9e0eab3b9'),
                'reportName': mock_get_full_path_response,
                'findings': 10,
                'filesWithFindings': 9,
                'generatedOn': mocked_datetime
            }
        ],
        'moreReportsPath': '-'
    }


# TestCase: 11
def test_get_doc_report_metadata(loader_helper):
    # Define static input
    doc = {"doc": "sample doc", "entities": {"Credit card number": 1, "aws access key": 1}, "entityCount": 2,
           "topicCount": 1,
           "topics": {"Medical Advice": 1}, "fileOwner": "pytest_file_owner", "sourceSize": 1000,
           "sourcePath": "/home/ubuntu/sens_data.csv"}
    get_finding_details_response = {}
    loader_helper._get_finding_details = MagicMock(return_value=get_finding_details_response)

    output = loader_helper._get_doc_report_metadata(doc, raw_data)
    assert output["total_findings"] == 3
    assert output["findings_entities"] == 2
    assert output["findings_topics"] == 1
    assert output["data_source_count"] == 1
    assert output["file_count"] == 1
    assert output["snippet_count"] == 1
    assert output["snippet_counter"] == 0
    assert output["total_snippet_counter"] == 0
    assert output["data_source_findings"] == {}
    assert output["loader_source_snippets"] == {
        '/home/ubuntu/sens_data.csv': {
            'findings_entities': 2,
            'findings_topics': 1,
            'findings': 3,
            'fileOwner': 'pytest_file_owner',
            'sourceSize': 1000
        }
    }


# TestCase: 12
def test_generate_final_report(loader_helper):
    # Mock Methods
    loader_helper._count_files_with_findings = MagicMock(return_value=10)
    loader_helper._create_report_summary = MagicMock(return_value=Summary(findings=3,
                                                                          findingsEntities=2,
                                                                          findingsTopics=1,
                                                                          totalFiles=1,
                                                                          filesWithFindings=4,
                                                                          dataSources=1,
                                                                          owner="fileOwner",
                                                                          createdAt=mocked_datetime))
    loader_helper._get_top_n_findings = MagicMock(return_value=[
        {
            'fileName': '/home/ubuntu/sens_data.csv',
            'fileOwner': 'fileOwner',
            'sourceSize': 1000,
            'findingsEntities': 2,
            'findingsTopics': 1,
            'findings': 3
        }
    ])
    loader_helper._get_data_source_details = MagicMock(return_value=[DataSource(name='CSVloader',
                                                                                sourcePath='sourcePath',
                                                                                sourceType='sourceType',
                                                                                sourceSize=1000,
                                                                                totalSnippetCount=0,
                                                                                displayedSnippetCount=0,
                                                                                findingsSummary=[],
                                                                                findingsDetails=[])])

    loader_helper._get_load_history = MagicMock(return_value=[])

    output = loader_helper._generate_final_report(raw_data={})
    assert output["name"] == "UnitTestApp"
    assert output["description"] == ""
    assert output["framework"] == {
        'name': 'langchain',
        'version': '0.1.16'
    }
    assert output["reportSummary"] == {
        'findings': 3,
        'findingsEntities': 2,
        'findingsTopics': 1,
        'totalFiles': 1,
        'filesWithFindings': 4,
        'dataSources': 1,
        'owner': 'fileOwner',
        'createdAt': mocked_datetime
    }
    assert output["loadHistory"] == {}
    assert output["topFindings"] == [
        {
            'fileName': '/home/ubuntu/sens_data.csv',
            'fileOwner': 'fileOwner',
            'sourceSize': 1000,
            'findingsEntities': 2,
            'findingsTopics': 1,
            'findings': 3
        }
    ]
    assert output["dataSources"] == [
        {
            'name': 'CSVloader',
            'sourcePath': 'sourcePath',
            'sourceType': 'sourceType',
            'sourceSize': 1000,
            'totalSnippetCount': 0,
            'displayedSnippetCount': 0,
            'findingsSummary': [

            ],
            'findingsDetails': [

            ]
        }
    ]
