import datetime

from pebblo.app.service.doc_helper import LoaderHelper

app_details = {
    "metadata": {
        "createdAt": "2024-09-19 11:41:18.192182",
        "modifiedAt": "2024-09-19 11:41:18.192183",
    },
    "name": "UnitTestApp",
    "description": "Loader App using Pebblo",
    "owner": "AppOwner",
    "pluginVersion": "0.1.1",
    "instanceDetails": {
        "type": "desktop",
        "host": "AppOwner-MBP",
        "path": "/home/data/scripts",
        "runtime": "Mac OSX",
        "ip": "192.168.1.39",
        "language": "python",
        "languageVersion": "3.11.9",
        "platform": "macOS-14.6.1-arm64-i386-64bit",
        "os": "Darwin",
        "osVersion": "Darwin Kernel Version 23.6.0: Mon Jul 29 21:13:04 PDT 2024; root:xnu-10063.141.2~1/RELEASE_ARM64_T6020",
        "createdAt": "2024-09-19 11:41:18.192116",
    },
    "framework": {"name": "langchain", "version": "0.2.35"},
    "lastUsed": "2024-09-19 11:41:18.192181",
    "pebbloServerVersion": "0.1.19",
    "pebbloClientVersion": "0.1.1",
    "clientVersion": {"name": "langchain_community", "version": "0.2.12"},
    "loaders": [
        {
            "name": "TextLoader",
            "sourcePath": "/home/data/sample.txt",
            "sourceType": "unsupported",
            "sourceSize": 211,
            "sourceFiles": [],
            "lastModified": datetime.datetime.now(),
        }
    ],
}

classifier_response_input_doc = {
    "doc": "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA. His American express credit card number is\n371449635398431. AWS Access Key AKIAQIPT4PDORIRTV6PH. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
    "source_path": "/home/data/sens_data.csv",
    "last_modified": datetime.datetime.now(),
    "file_owner": "fileOwner",
    "source_path_size": 211,
}

data = {
    "name": "UnitTestApp",
    "owner": "AppOwner",
    "docs": [classifier_response_input_doc],
    "plugin_version": "0.1.1",
    "load_id": "26db970f-b4c6-44ae-9235-8f18236695a1",
    "loader_details": {
        "loader": "TextLoader",
        "source_path": "/home/data/sample.txt",
        "source_type": "unsupported",
        "source_path_size": "211",
        "source_aggregate_size": 211,
    },
    "loading_end": True,
    "source_owner": "AppOwner",
    "classifier_location": "local",
    "classifier_mode": None,
    "anonymize_snippets": None,
}

expected_output = {
    "data": "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA. His American express credit card number is\n371449635398431. AWS Access Key AKIAQIPT4PDORIRTV6PH. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
    "entityCount": 3,
    "entities": {"us-ssn": 1, "credit-card-number": 1, "aws-access-key": 1},
    "entityDetails": {
        "us-ssn": [
            {
                "location": "16_27",
                "confidence_score": "HIGH",
                "entity_group": "pii-identification",
            }
        ],
        "credit-card-number": [
            {
                "location": "102_117",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "aws-access-key": [
            {
                "location": "134_154",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
    },
    "topicCount": 0,
    "topics": {},
    "topicDetails": {},
}


def test_get_classifier_response():
    loader_helper = LoaderHelper(app_details, data=data, load_id=data.get("load_id"))
    output = loader_helper._get_classifier_response(classifier_response_input_doc)
    expected_output = {
        "data": "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA. His American express credit card number is\n371449635398431. AWS Access Key AKIAQIPT4PDORIRTV6PH. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
        "entityCount": 3,
        "entities": {"us-ssn": 1, "credit-card-number": 1, "aws-access-key": 1},
        "entityDetails": {
            "us-ssn": [
                {
                    "location": "16_27",
                    "confidence_score": "HIGH",
                    "entity_group": "pii-identification",
                }
            ],
            "credit-card-number": [
                {
                    "location": "102_117",
                    "confidence_score": "HIGH",
                    "entity_group": "pii-financial",
                }
            ],
            "aws-access-key": [
                {
                    "location": "134_154",
                    "confidence_score": "HIGH",
                    "entity_group": "secrets_and_tokens",
                }
            ],
        },
        "topicCount": 1,
        "topics": {"financial": 1},
        "topicDetails": {"financial": [{"confidence_score": "MEDIUM"}]},
    }
    assert output.model_dump() == expected_output


def test_get_classifier_response_classifier_mode_entity():
    loader_helper_classifier_mode_entity = LoaderHelper(
        app_details, data=data, load_id=data.get("load_id"), classifier_mode="entity"
    )
    output = loader_helper_classifier_mode_entity._get_classifier_response(
        classifier_response_input_doc
    )

    assert output.model_dump() == expected_output


def test_get_classifier_response_classifier_mode_topic():
    loader_helper_classifier_mode_topic = LoaderHelper(
        app_details, data=data, load_id=data.get("load_id"), classifier_mode="topic"
    )
    output = loader_helper_classifier_mode_topic._get_classifier_response(
        classifier_response_input_doc
    )
    expected_output.update(
        {
            "data": "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA. His American express credit card number is\n371449635398431. AWS Access Key AKIAQIPT4PDORIRTV6PH. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
            "entityCount": 0,
            "entities": {},
            "entityDetails": {},
            "topicCount": 1,
            "topics": {"financial": 1},
            "topicDetails": {"financial": [{"confidence_score": "MEDIUM"}]},
        }
    )
    assert output.model_dump() == expected_output


def test_get_classifier_response_anonymize_true():
    loader_helper_anonymize_true = LoaderHelper(
        app_details, data=data, load_id=data.get("load_id"), anonymize_snippets=True
    )
    output = loader_helper_anonymize_true._get_classifier_response(
        classifier_response_input_doc
    )

    expected_output.update(
        {
            "data": "Sachin's SSN is &lt;US_SSN&gt;. His passport ID is 5484880UA. His American express credit card number is\n&lt;CREDIT_CARD&gt;. AWS Access Key &lt;AWS_ACCESS_KEY&gt;. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
            "entityCount": 3,
            "entities": {"us-ssn": 1, "credit-card-number": 1, "aws-access-key": 1},
            "entityDetails": {
                "us-ssn": [
                    {
                        "location": "16_30",
                        "confidence_score": "HIGH",
                        "entity_group": "pii-identification",
                    }
                ],
                "credit-card-number": [
                    {
                        "location": "105_124",
                        "confidence_score": "HIGH",
                        "entity_group": "pii-financial",
                    }
                ],
                "aws-access-key": [
                    {
                        "location": "141_163",
                        "confidence_score": "HIGH",
                        "entity_group": "secrets_and_tokens",
                    }
                ],
            },
            "topicCount": 1,
            "topics": {"financial": 1},
            "topicDetails": {"financial": [{"confidence_score": "MEDIUM"}]},
        }
    )
    assert output.model_dump() == expected_output
