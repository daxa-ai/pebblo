from unittest.mock import Mock, patch

import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.test_data import input_text1, input_text2, negative_data


class TestOperatorResult:
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


@pytest.fixture
def mocked_presidio_entity_response(mocker):
    """
    Mocking entity classifier response
    """
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response",
        return_value=Mock(),
    )

    anomyze_response1 = [
        TestOperatorResult("PERSON"),
        TestOperatorResult("US_ITIN"),
        TestOperatorResult("US_SSN"),
        TestOperatorResult("PERSON"),
    ]
    anomyze_response2 = [
        TestOperatorResult("US_SSN"),
        TestOperatorResult("US_ITIN"),
        TestOperatorResult("IBAN_CODE"),
        TestOperatorResult("CREDIT_CARD"),
    ]
    anomyze_response3 = [
        TestOperatorResult("US_SSN"),
        TestOperatorResult("CREDIT_CARD"),
    ]
    anomyze_response4 = [
        TestOperatorResult("PERSON"),
        TestOperatorResult("PERSON"),
    ]
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response",
        side_effect=[
            anomyze_response1,
            anomyze_response2,
            anomyze_response3,
            anomyze_response4,
        ],
    )


@pytest.fixture
def mocked_presidio_secret_response(mocker):
    """
    Mocking secret entity classifier response
    """
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response",
        return_value=Mock(),
    )

    anomyze_response1 = [
        TestOperatorResult("GITHUB_TOKEN"),
        TestOperatorResult("AWS_ACCESS_KEY"),
    ]
    anomyze_response2 = [
        TestOperatorResult("SLACK_TOKEN"),
        TestOperatorResult("SLACK_TOKEN"),
        TestOperatorResult("GITHUB_TOKEN"),
        TestOperatorResult("AWS_SECRET_KEY"),
        TestOperatorResult("AWS_ACCESS_KEY"),
    ]
    anomyze_response3 = []
    mocker.patch(
        "pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response",
        side_effect=[anomyze_response1, anomyze_response2, anomyze_response3],
    )


@pytest.fixture
def entity_classifier(mocked_objects):
    """
    Create an instance of the EntityClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init(mocked_objects) -> None:
    _ = EntityClassifier()


def test_presidio_entity_classifier(entity_classifier, mocked_presidio_entity_response):
    """
    UTs for presidio_entity_classifier function
    """
    entities, total_count = entity_classifier.presidio_entity_classifier(input_text1)
    assert entities == {"US ITIN": 1, "US SSN": 1}
    assert total_count == 2

    entities, total_count = entity_classifier.presidio_entity_classifier(input_text2)
    assert entities == {
        "US ITIN": 1,
        "IBAN code": 1,
        "Credit card number": 1,
        "US SSN": 1,
    }
    assert total_count == 4

    entities, total_count = entity_classifier.presidio_entity_classifier(input_text2)
    assert entities == {"Credit card number": 1, "US SSN": 1}
    assert total_count == 2

    entities, total_count = entity_classifier.presidio_entity_classifier(negative_data)
    assert entities == {}
    assert total_count == 0


def test_presidio_secret_entity_classifier(
    entity_classifier, mocked_presidio_secret_response
):
    """
    UTs for presidio_secret_classifier function
    """
    secret_entities, total_count = entity_classifier.presidio_secret_classifier(
        input_text1
    )
    assert secret_entities == {"AWS Access Key": 1, "Github Token": 1}
    assert total_count == 2

    secret_entities, total_count = entity_classifier.presidio_secret_classifier(
        input_text2
    )
    assert secret_entities == {
        "Slack Token": 2,
        "Github Token": 1,
        "AWS Secret Key": 1,
        "AWS Access Key": 1,
    }
    assert total_count == 5

    secret_entities, total_count = entity_classifier.presidio_secret_classifier(
        negative_data
    )
    assert secret_entities == {}
    assert total_count == 0
