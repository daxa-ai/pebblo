from unittest.mock import patch
from unittest.mock import Mock
import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.test_data import input_text1, input_text2


class TestOperatorResult:
    def __init__(self, entity_type):
        self.entity_type = entity_type


@pytest.fixture
def mocked_objects():
    with patch('pebblo.entity_classifier.entity_classifier.AnalyzerEngine') as mock_analyzer, \
            patch('pebblo.entity_classifier.entity_classifier.AnalyzerEngine') as mock_anomyzer, \
            patch('pebblo.entity_classifier.utils.utils.add_custom_regex_analyzer_registry') as mock_custom_registry:
        yield mock_analyzer, mock_anomyzer, mock_custom_registry


@pytest.fixture
def mocked_presidio_entity_response1(mocker):
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response',
        return_value=Mock()
    )

    anomyze_response = [
        TestOperatorResult('PERSON'),
        TestOperatorResult('US_ITIN'),
        TestOperatorResult('US_SSN'),
        TestOperatorResult('PERSON'),
    ]
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response',
        return_value=anomyze_response
    )


@pytest.fixture
def mocked_presidio_secret_response1(mocker):
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response',
        return_value=Mock()
    )

    anomyze_response = [
        TestOperatorResult('GITHUB_TOKEN'),
        TestOperatorResult('AWS_ACCESS_KEY'),
    ]
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response',
        return_value=anomyze_response
    )


@pytest.fixture
def mocked_presidio_entity_response2(mocker):
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response',
        return_value=Mock()
    )

    anomyze_response = [
        TestOperatorResult('US_SSN'),
        TestOperatorResult('US_ITIN'),
        TestOperatorResult('IBAN_CODE'),
        TestOperatorResult('CREDIT_CARD'),
    ]
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response',
        return_value=anomyze_response
    )


@pytest.fixture
def mocked_presidio_secret_response2(mocker):
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response',
        return_value=Mock()
    )

    anomyze_response = [
        TestOperatorResult('SLACK_TOKEN'),
        TestOperatorResult('SLACK_TOKEN'),
        TestOperatorResult('GITHUB_TOKEN'),
        TestOperatorResult('AWS_SECRET_KEY'),
        TestOperatorResult('AWS_ACCESS_KEY'),
    ]
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response',
        return_value=anomyze_response
    )


@pytest.fixture
def mocked_presidio_entity_response3(mocker):
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.analyze_response',
        return_value=Mock()
    )

    anomyze_response = [
        TestOperatorResult('US_SSN'),
        TestOperatorResult('CREDIT_CARD'),
    ]
    mocker.patch(
        'pebblo.entity_classifier.entity_classifier.EntityClassifier.anomyze_response',
        return_value=anomyze_response
    )


@pytest.fixture
def entity_classifier(mocked_objects):
    """
    Create an instance of the EntityClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init(mocked_objects) -> None:
    _ = EntityClassifier()


def test_presidio_entity_classifier1(entity_classifier, mocked_presidio_entity_response1):
    entities, total_count = entity_classifier.presidio_entity_classifier(input_text1)
    assert entities == {'US ITIN': 1, 'US SSN': 1}
    assert total_count == 2


def test_presidio_secret_entity_classifier1(entity_classifier, mocked_presidio_secret_response1):
    secret_entities, total_count = entity_classifier.presidio_secret_classifier(input_text1)
    assert secret_entities == {'AWS Access Key': 1, 'Github Token': 1}
    assert total_count == 2


def test_presidio_entity_classifier2(entity_classifier, mocked_presidio_entity_response2):
    entities, total_count = entity_classifier.presidio_entity_classifier(input_text2)
    assert entities == {'US ITIN': 1, 'IBAN code': 1, 'Credit card number': 1, 'US SSN': 1}
    assert total_count == 4


def test_presidio_secret_entity_classifier2(entity_classifier, mocked_presidio_secret_response2):
    secret_entities, total_count = entity_classifier.presidio_secret_classifier(input_text2)
    assert secret_entities == {'Slack Token': 2, 'Github Token': 1, 'AWS Secret Key': 1, 'AWS Access Key': 1}
    assert total_count == 5


def test_presidio_entity_classifier3(entity_classifier, mocked_presidio_entity_response3):
    entities, total_count = entity_classifier.presidio_entity_classifier(input_text2)
    assert entities == {'Credit card number': 1, 'US SSN': 1}
    assert total_count == 2
