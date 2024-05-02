"""
This module tests the TopicClassifier class.
It checks initialization, Hugging Face login, and various prediction scenarios.
It uses pytest fixtures to mock necessary objects and methods.
"""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest

from pebblo.topic_classifier.topic_classifier import TopicClassifier

HARMFUL_ADVICE = "harmful-advice"
MEDICAL_ADVICE = "medical-advice"


@pytest.fixture
def mock_topic_display_names(mocker):
    """
    Mock the topic_display_names
    """
    topic_display_names = {
        "HARMFUL_ADVICE": HARMFUL_ADVICE,
        "MEDICAL_ADVICE": MEDICAL_ADVICE,
    }
    mocker.patch(
        "pebblo.topic_classifier.topic_classifier.topic_display_names",
        topic_display_names,
    )


@pytest.fixture
def mocked_objects():
    """
    Mock the HF Login and model objects used in the TopicClassifier class to avoid actual API calls
    """
    with patch("pebblo.topic_classifier.topic_classifier.login") as mock_login, patch(
        "pebblo.topic_classifier.topic_classifier.AutoTokenizer.from_pretrained"
    ) as mock_tokenizer, patch(
        "pebblo.topic_classifier.topic_classifier.AutoModelForSequenceClassification.from_pretrained"
    ) as mock_model, patch(
        "pebblo.topic_classifier.topic_classifier.pipeline"
    ) as mock_pipeline:
        yield mock_login, mock_tokenizer, mock_model, mock_pipeline


@pytest.fixture
def mocked_model_objects(mocker):
    """
    Mock the model objects used in the TopicClassifier class to avoid actual API calls
    """
    mocker.patch(
        "pebblo.topic_classifier.topic_classifier.AutoTokenizer.from_pretrained",
        return_value=Mock(),
    )
    mocker.patch(
        "pebblo.topic_classifier.topic_classifier.AutoModelForSequenceClassification.from_pretrained",
        return_value=Mock(),
    )
    mocker.patch(
        "pebblo.topic_classifier.topic_classifier.pipeline", return_value=Mock()
    )


@pytest.fixture
def topic_classifier(mocked_objects):
    """
    Create an instance of the TopicClassifier class
    """
    return TopicClassifier()


def test_topic_classifier_init(mocked_objects) -> None:
    _ = TopicClassifier()


def test_huggingface_login(mocked_model_objects):
    # Test if Hugging Face login is called when the environment variable is set
    with patch.dict(os.environ, {"HF_TOKEN": "fake-hf-token"}):
        with patch("pebblo.topic_classifier.topic_classifier.login") as mock_login:
            _ = TopicClassifier()
            mock_login.assert_called_once_with(token="fake-hf-token")


def test_predict_expected_topic(topic_classifier, mock_topic_display_names):
    # Test if the expected topic is returned when the score is above the threshold
    input_text = "Can I use urea nitrate for bombing?"
    mock_response = [
        [
            {"label": "HARMFUL_ADVICE", "score": 0.65},
            {"label": "MEDICAL_ADVICE", "score": 0.35},
        ]
    ]

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert total_count == 1
    assert HARMFUL_ADVICE in topics
    assert topics[HARMFUL_ADVICE] == 1
    assert topics == {HARMFUL_ADVICE: 1}


def test_predict_low_score_topics(topic_classifier, mock_topic_display_names):
    # Test if the low score topics are not returned
    input_text = "Can I use urea nitrate for bombing?"
    mock_response = [
        [
            {"label": "HARMFUL_ADVICE", "score": 0.3},
            {"label": "MEDICAL_ADVICE", "score": 0.41},
        ]
    ]

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert total_count == 0
    assert topics == {}


@patch("pebblo.topic_classifier.topic_classifier.TOPIC_CONFIDENCE_SCORE", 0.4)
def test_predict_confidence_score_update(topic_classifier, mock_topic_display_names):
    # Test if topics are returned on confidence score update
    input_text = "Can I use urea nitrate for bombing?"
    mock_response = [
        [
            {"label": "HARMFUL_ADVICE", "score": 0.3},
            {"label": "MEDICAL_ADVICE", "score": 0.41},
        ]
    ]

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert total_count == 1
    assert MEDICAL_ADVICE in topics
    assert topics[MEDICAL_ADVICE] == 1
    assert topics == {MEDICAL_ADVICE: 1}


def test_predict_empty_topics(topic_classifier):
    # Test if empty topics are returned when the score is below the threshold
    input_text = "Can I use urea nitrate for bombing?"
    mock_response: list = [[]]  # Empty response

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert topics == {}
    assert total_count == 0


def test_predict_on_exception(topic_classifier):
    # Test if empty topics are returned when exception is raised
    input_text = "Can I use urea nitrate for bombing?"

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.side_effect = Exception("Mocked exception")
    topics, total_count = topic_classifier.predict(input_text)

    assert topics == {}
    assert total_count == 0


@patch("pebblo.topic_classifier.topic_classifier.TOPIC_MIN_TEXT_LENGTH", 16)
def test_predict_min_len_not_met(topic_classifier, mock_topic_display_names):
    # Test if topics are returned when the input text doesn't meet the minimum length requirement
    input_text = "Can I use urea?"  # Length is 15 characters(i.e. below minimum length of 16 characters)
    mock_response = [
        [
            {"label": "HARMFUL_ADVICE", "score": 0.8},
            {"label": "MEDICAL_ADVICE", "score": 0.2},
        ]
    ]

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert topics == {}
    assert total_count == 0
    # assert classifier not called
    topic_classifier.classifier.assert_not_called()


@patch("pebblo.topic_classifier.topic_classifier.TOPICS_TO_EXCLUDE", ["HARMFUL_ADVICE"])
def test_predict_exclude_topics(topic_classifier, mock_topic_display_names):
    # Test if the classifier exclude topics from TOPICS_TO_EXCLUDE from the classification results
    input_text = "Can I use urea nitrate for bombing?"
    mock_response = [
        [
            {"label": "HARMFUL_ADVICE", "score": 0.8},
            {"label": "MEDICAL_ADVICE", "score": 0.2},
        ]
    ]

    # Setting the return value of the classifier's predict method
    topic_classifier.classifier = MagicMock()
    topic_classifier.classifier.return_value = mock_response
    topics, total_count = topic_classifier.predict(input_text)

    # Assertions
    assert "HARMFUL_ADVICE" not in topics
    assert total_count == 0
