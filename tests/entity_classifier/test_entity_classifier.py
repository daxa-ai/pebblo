from typing import List, Tuple
from unittest.mock import Mock, patch

import pytest

import tests.log  # noqa: F401
from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.mock_response import (
    mock_input_text1_anonymize_snippet_true,
    mock_input_text2_anonymize_snippet_true,
)
from tests.entity_classifier.test_data import input_text1, input_text2, negative_data


class TestAnonymizerResult:
    def __init__(self, entity_type):
        self.entity_type = entity_type


@pytest.fixture
def mocked_objects():
    with (
        patch(
            "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
        ) as mock_analyzer,
        patch(
            "pebblo.entity_classifier.entity_classifier.AnalyzerEngine"
        ) as mock_anomyzer,
        patch(
            "pebblo.entity_classifier.utils.utils.add_custom_regex_analyzer_registry"
        ) as mock_custom_registry,
    ):
        yield mock_analyzer, mock_anomyzer, mock_custom_registry


@pytest.fixture
def mocked_entity_classifier_response(mocker):
    """
    Mocking entity classifier response
    """
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response",
        return_value=Mock(),
    )

    anonymize_response1: Tuple[list, str] = (
        [
            TestAnonymizerResult("GITHUB_TOKEN"),
            TestAnonymizerResult("AWS_ACCESS_KEY"),
            TestAnonymizerResult("US_ITIN"),
            TestAnonymizerResult("US_SSN"),
        ],
        mock_input_text1_anonymize_snippet_true,
    )
    anonymize_response2: Tuple[list, str] = (
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
        mock_input_text2_anonymize_snippet_true,
    )
    anonymize_negative_response: Tuple[list, str] = (
        [],
        negative_data,
    )
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.anonymize_response",
        side_effect=[
            anonymize_response1,
            anonymize_response2,
            anonymize_negative_response,
        ],
    )

    analyzed_entities_response1: List[dict] = [
        {"entity_type": "US_SSN", "location": "17_28", "confidence_score": 0.85},
        {"entity_type": "US_ITIN", "location": "42_53", "confidence_score": 0.85},
        {
            "entity_type": "AWS_ACCESS_KEY",
            "location": "77_97",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "GITHUB_TOKEN",
            "location": "120_210",
            "confidence_score": 0.8,
        },
    ]
    analyzed_entities_response2: List[dict] = [
        {"entity_type": "US_SSN", "location": "17_25", "confidence_score": 0.85},
        {"entity_type": "US_ITIN", "location": "39_48", "confidence_score": 0.85},
        {
            "entity_type": "AWS_ACCESS_KEY",
            "location": "72_88",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "GITHUB_TOKEN",
            "location": "111_125",
            "confidence_score": 0.8,
        },
    ]
    analyzed_entities_response3: List[dict] = [
        {
            "entity_type": "CREDIT_CARD",
            "location": "1367_1382",
            "confidence_score": 1.0,
        },
        {
            "entity_type": "IBAN_CODE",
            "location": "1406_1434",
            "confidence_score": 1.0,
        },
        {"entity_type": "US_SSN", "location": "1178_1189", "confidence_score": 0.85},
        {"entity_type": "US_ITIN", "location": "1450_1461", "confidence_score": 0.85},
        {
            "entity_type": "AWS_ACCESS_KEY",
            "location": "1545_1565",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "AWS_SECRET_KEY",
            "location": "1587_1628",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "GITHUB_TOKEN",
            "location": "1646_1736",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "SLACK_TOKEN",
            "location": "1812_1835",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "SLACK_TOKEN",
            "location": "1911_1968",
            "confidence_score": 0.8,
        },
    ]
    analyzed_entities_response4: List[dict] = [
        {
            "entity_type": "CREDIT_CARD",
            "location": "1178_1186",
            "confidence_score": 1.0,
        },
        {
            "entity_type": "IBAN_CODE",
            "location": "1364_1377",
            "confidence_score": 1.0,
        },
        {"entity_type": "US_SSN", "location": "1401_1412", "confidence_score": 0.85},
        {"entity_type": "US_ITIN", "location": "1428_1437", "confidence_score": 0.85},
        {
            "entity_type": "AWS_ACCESS_KEY",
            "location": "1521_1537",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "AWS_SECRET_KEY",
            "location": "1559_1575",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "GITHUB_TOKEN",
            "location": "1593_1607",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "SLACK_TOKEN",
            "location": "1683_1696",
            "confidence_score": 0.8,
        },
        {
            "entity_type": "SLACK_TOKEN",
            "location": "1772_1785",
            "confidence_score": 0.8,
        },
    ]
    analyzed_entities_negative_response1: List = []
    analyzed_entities_negative_response2: List = []
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.get_analyzed_entities_response",
        side_effect=[
            analyzed_entities_response1,
            analyzed_entities_response2,
            analyzed_entities_response3,
            analyzed_entities_response4,
            analyzed_entities_negative_response1,
            analyzed_entities_negative_response2,
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
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1)
    assert entities == {
        "github-token": 1,
        "aws-access-key": 1,
        "us-itin": 1,
        "us-ssn": 1,
    }
    assert total_count == 4
    assert anonymized_text == input_text1
    assert entity_details == {
        "us-ssn": [{"location": "17_28", "confidence_score": "HIGH"}],
        "us-itin": [{"location": "42_53", "confidence_score": "HIGH"}],
        "aws-access-key": [{"location": "77_97", "confidence_score": "HIGH"}],
        "github-token": [{"location": "120_210", "confidence_score": "HIGH"}],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1, True)
    assert entities == {
        "github-token": 1,
        "aws-access-key": 1,
        "us-itin": 1,
        "us-ssn": 1,
    }
    assert total_count == 4
    assert anonymized_text == mock_input_text1_anonymize_snippet_true
    assert entity_details == {
        "us-ssn": [{"location": "17_25", "confidence_score": "HIGH"}],
        "us-itin": [{"location": "39_48", "confidence_score": "HIGH"}],
        "aws-access-key": [{"location": "72_88", "confidence_score": "HIGH"}],
        "github-token": [{"location": "111_125", "confidence_score": "HIGH"}],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text2)
    assert entities == {
        "slack-token": 2,
        "github-token": 1,
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "us-itin": 1,
        "iban-code": 1,
        "credit-card-number": 1,
        "us-ssn": 1,
    }
    assert total_count == 9
    assert anonymized_text == input_text2
    assert entity_details == {
        "credit-card-number": [{"location": "1367_1382", "confidence_score": "HIGH"}],
        "iban-code": [{"location": "1406_1434", "confidence_score": "HIGH"}],
        "us-ssn": [{"location": "1178_1189", "confidence_score": "HIGH"}],
        "us-itin": [{"location": "1450_1461", "confidence_score": "HIGH"}],
        "aws-access-key": [{"location": "1545_1565", "confidence_score": "HIGH"}],
        "aws-secret-key": [{"location": "1587_1628", "confidence_score": "HIGH"}],
        "github-token": [{"location": "1646_1736", "confidence_score": "HIGH"}],
        "slack-token": [
            {"location": "1812_1835", "confidence_score": "HIGH"},
            {"location": "1911_1968", "confidence_score": "HIGH"},
        ],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text2, anonymize_snippets=True
    )
    assert entities == {
        "slack-token": 2,
        "github-token": 1,
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "us-itin": 1,
        "iban-code": 1,
        "credit-card-number": 1,
        "us-ssn": 1,
    }
    assert total_count == 9
    assert anonymized_text == mock_input_text2_anonymize_snippet_true
    assert entity_details == {
        "credit-card-number": [{"location": "1178_1186", "confidence_score": "HIGH"}],
        "iban-code": [{"location": "1364_1377", "confidence_score": "HIGH"}],
        "us-ssn": [{"location": "1401_1412", "confidence_score": "HIGH"}],
        "us-itin": [{"location": "1428_1437", "confidence_score": "HIGH"}],
        "aws-access-key": [{"location": "1521_1537", "confidence_score": "HIGH"}],
        "aws-secret-key": [{"location": "1559_1575", "confidence_score": "HIGH"}],
        "github-token": [{"location": "1593_1607", "confidence_score": "HIGH"}],
        "slack-token": [
            {"location": "1683_1696", "confidence_score": "HIGH"},
            {"location": "1772_1785", "confidence_score": "HIGH"},
        ],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(negative_data)
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        negative_data, anonymize_snippets=True
    )
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data
