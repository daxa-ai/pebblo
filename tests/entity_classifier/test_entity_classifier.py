from unittest.mock import Mock, patch

import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.mock_response import (
    mock_input_text1_all_entity_false,
    mock_input_text1_all_entity_true,
    mock_input_text2_all_entity_false,
    mock_input_text2_all_entity_true,
    mock_negative_data_all_entity_false,
    mock_negative_data_all_entity_true,
)
from tests.entity_classifier.test_data import input_text1, input_text2, negative_data


class TestAnonymizerResult:
    def __init__(self, entity_type):
        self.entity_type = entity_type


@pytest.fixture
def mocked_objects():
    with patch(
        "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
    ) as mock_analyzer, patch(
        "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
    ) as mock_anomyzer, patch(
        "pebblo.entity_classifier.utils.utils.add_custom_regex_analyzer_registry"
    ) as mock_custom_registry:
        yield mock_analyzer, mock_anomyzer, mock_custom_registry


@pytest.fixture()
def mocked_entity_classifier_response(mocker):
    """
    Mocking entity classifier response
    """
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response",
        return_value=Mock(),
    )

    anonymize_response1 = (
        [
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("GITHUB_TOKEN"),
            TestAnonymizerResult("AWS_ACCESS_KEY"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("US_ITIN"),
            TestAnonymizerResult("US_SSN"),
        ],
        mock_input_text1_all_entity_false,
    )

    anonymize_response2 = (
        [
            TestAnonymizerResult("GITHUB_TOKEN"),
            TestAnonymizerResult("AWS_ACCESS_KEY"),
            TestAnonymizerResult("US_ITIN"),
            TestAnonymizerResult("US_SSN"),
        ],
        mock_input_text1_all_entity_true,
    )

    anonymize_response3 = (
        [
            TestAnonymizerResult("SLACK_TOKEN"),
            TestAnonymizerResult("SLACK_TOKEN"),
            TestAnonymizerResult("GITHUB_TOKEN"),
            TestAnonymizerResult("AWS_SECRET_KEY"),
            TestAnonymizerResult("AWS_ACCESS_KEY"),
            TestAnonymizerResult("US_ITIN"),
            TestAnonymizerResult("IBAN_CODE"),
            TestAnonymizerResult("CREDIT_CARD"),
            TestAnonymizerResult("US_SSN"),
        ],
        mock_input_text2_all_entity_false,
    )

    anonymize_response4 = (
        [
            TestAnonymizerResult("SLACK_TOKEN"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("SLACK_TOKEN"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("GITHUB_TOKEN"),
            TestAnonymizerResult("AWS_SECRET_KEY"),
            TestAnonymizerResult("AWS_ACCESS_KEY"),
            TestAnonymizerResult("US_ITIN"),
            TestAnonymizerResult("IBAN_CODE"),
            TestAnonymizerResult("CREDIT_CARD"),
            TestAnonymizerResult("NRP"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("NRP"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("US_SSN"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("PERSON"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("DATE_TIME"),
            TestAnonymizerResult("PERSON"),
        ],
        mock_input_text2_all_entity_true,
    )

    anonymize_negative_response1 = (
        [],
        mock_negative_data_all_entity_true,
    )

    anonymize_negative_response2 = (
        [],
        mock_negative_data_all_entity_false,
    )

    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.anonymize_response",
        side_effect=[
            anonymize_response1,
            anonymize_response2,
            anonymize_response3,
            anonymize_response4,
            anonymize_negative_response1,
            anonymize_negative_response2,
        ],
    )


@pytest.fixture
def entity_classifier(mocked_objects):
    """
    Create an instance of the EntityClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init(mocked_objects) -> None:
    """
    Initiated Entity Classifier
    """
    _ = EntityClassifier()


def test_presidio_entity_classifier_and_anonymizer(
    entity_classifier, mocked_entity_classifier_response
):
    """
    UTs for presidio_entity_classifier_and_anonymizer function
    """
    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1)
    assert entities == {
        "Github Token": 1,
        "AWS Access Key": 1,
        "US ITIN": 1,
        "US SSN": 1,
    }
    assert total_count == 4
    assert anonymized_text == mock_input_text1_all_entity_false

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text1,anonymize_all_entities=False
    )
    assert entities == {
        "Github Token": 1,
        "AWS Access Key": 1,
        "US ITIN": 1,
        "US SSN": 1,
    }
    assert total_count == 4
    assert anonymized_text == mock_input_text1_all_entity_true

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text2)
    assert entities == {
        "Slack Token": 2,
        "Github Token": 1,
        "AWS Access Key": 1,
        "AWS Secret Key": 1,
        "US ITIN": 1,
        "IBAN code": 1,
        "Credit card number": 1,
        "US SSN": 1,
    }

    assert total_count == 9
    assert anonymized_text == mock_input_text2_all_entity_false

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text1,anonymize_all_entities=False
    )
    assert entities == {
        "Slack Token": 2,
        "Github Token": 1,
        "AWS Access Key": 1,
        "AWS Secret Key": 1,
        "US ITIN": 1,
        "IBAN code": 1,
        "Credit card number": 1,
        "US SSN": 1,
    }
    assert total_count == 9
    assert anonymized_text == mock_input_text2_all_entity_true

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        negative_data,anonymize_all_entities=True
    )
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == mock_negative_data_all_entity_true

    (
        entities,
        total_count,
        anonymized_text,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        negative_data,anonymize_all_entities=False
    )
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == mock_negative_data_all_entity_false
