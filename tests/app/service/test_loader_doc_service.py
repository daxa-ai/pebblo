import datetime

import pytest

from pebblo.app.enums.common import ClassificationMode
from pebblo.app.service.loader.loader_doc_service import AppLoaderDoc

classifier_response_input_doc = {
    "doc": "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA. His American express credit card number is\n371449635398431. AWS Access Key AKIAQIPT4PDORIRTV6PH. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
    "source_path": "/home/data/sens_data.csv",
    "last_modified": datetime.datetime.now(),
    "file_owner": "fileOwner",
    "source_path_size": 211,
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


@pytest.fixture
def app_loader_helper():
    return AppLoaderDoc()


def test_get_classifier_response(app_loader_helper):
    app_loader_helper.classifier_mode = ClassificationMode.ALL.value
    app_loader_helper.anonymize_snippets = False
    output = app_loader_helper._get_doc_classification(classifier_response_input_doc)
    assert output.model_dump() == expected_output


def test_get_classifier_response_classifier_mode_entity(app_loader_helper):
    app_loader_helper.classifier_mode = ClassificationMode.ENTITY.value
    app_loader_helper.anonymize_snippets = False
    output = app_loader_helper._get_doc_classification(classifier_response_input_doc)
    assert output.model_dump() == expected_output


def test_get_classifier_response_classifier_mode_topic(app_loader_helper):
    app_loader_helper.classifier_mode = ClassificationMode.TOPIC.value
    app_loader_helper.anonymize_snippets = False
    output = app_loader_helper._get_doc_classification(classifier_response_input_doc)
    expected_output.update(
        {
            "entityCount": 0,
            "entities": {},
            "entityDetails": {},
        }
    )
    assert output.model_dump() == expected_output


def test_get_classifier_response_anonymize_true(app_loader_helper):
    app_loader_helper.classifier_mode = ClassificationMode.ALL.value
    app_loader_helper.anonymize_snippets = True
    output = app_loader_helper._get_doc_classification(classifier_response_input_doc)
    expected_output.update(
        {
            "data": "Sachin's SSN is &lt;US_SSN&gt;. His passport ID is 5484880UA. His American express credit card number is\n&lt;CREDIT_CARD&gt;. AWS Access Key &lt;AWS_ACCESS_KEY&gt;. client-secret is de1d4a2d-d9fa-44f1-84bb-4f73c004afda\n",
            "entities": {"aws-access-key": 1, "credit-card-number": 1, "us-ssn": 1},
            "entityCount": 3,
            "entityDetails": {
                "aws-access-key": [
                    {
                        "confidence_score": "HIGH",
                        "entity_group": "secrets_and_tokens",
                        "location": "141_163",
                    }
                ],
                "credit-card-number": [
                    {
                        "confidence_score": "HIGH",
                        "entity_group": "pii-financial",
                        "location": "105_124",
                    }
                ],
                "us-ssn": [
                    {
                        "confidence_score": "HIGH",
                        "entity_group": "pii-identification",
                        "location": "16_30",
                    }
                ],
            },
        }
    )
    assert output.model_dump() == expected_output
