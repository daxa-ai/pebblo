# test_prompt_gov.py
from unittest.mock import patch

import pytest

from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import AiDataModel
from pebblo.app.service.classification import Classification


@pytest.fixture
def mock_entity_classifier():
    with patch("pebblo.app.service.classification.EntityClassifier") as mock:
        yield mock


@pytest.fixture
def mock_topic_classifier():
    with patch("pebblo.app.service.classification.TopicClassifier") as mock:
        yield mock


def test_process_request_success(mock_entity_classifier, mock_topic_classifier):
    mock_entity_classifier_instance = mock_entity_classifier.return_value
    mock_entity_classifier_instance.presidio_entity_classifier_and_anonymizer.return_value = (
        {"us-ssn": 1},
        1,
        "anonymized document",
        {
            "us-ssn": [
                {
                    "location": "16_27",
                    "confidence_score": "HIGH",
                    "entity_group": "pii-identification",
                }
            ]
        },
    )

    mock_topic_classifier_instance = mock_topic_classifier.return_value
    mock_topic_classifier_instance.predict.return_value = ({}, 0, {})

    data = {"inputs": "Sachin's SSN is 222-85-4836"}
    cls_obj = Classification(data)
    response = cls_obj.process_request()
    expected_response = AiDataModel(
        data="",
        entities={"us-ssn": 1},
        entityCount=1,
        entityDetails={
            "us-ssn": [
                {
                    "location": "16_27",
                    "confidence_score": "HIGH",
                    "entity_group": "pii-identification",
                }
            ]
        },
        topics={},
        topicCount=0,
        topicDetails={},
    )
    expected_response = PebbloJsonResponse.build(
        body=expected_response.model_dump(exclude_none=True), status_code=200
    )

    assert response.status_code == expected_response.status_code
    assert response.body == expected_response.body