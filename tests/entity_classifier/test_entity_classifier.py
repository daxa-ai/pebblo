from unittest.mock import patch

import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier


@pytest.fixture
def mocked_objects():
    with patch('pebblo.entity_classifier.entity_classifier.AnalyzerEngine') as mock_analyzer, \
            patch('pebblo.entity_classifier.entity_classifier.AnalyzerEngine') as mock_anomyzer:
        yield mock_analyzer, mock_anomyzer


@pytest.fixture
def entity_classifier(mocked_objects):
    """
    Create an instance of the TopicClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init(mocked_objects) -> None:
    _ = EntityClassifier()
