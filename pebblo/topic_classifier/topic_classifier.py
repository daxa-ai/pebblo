"""
Module for topic classification using Pebblo and Hugging Face.
Defines the TopicClassifier class with methods for predicting topics and extracting them from the model's response.
"""

import os

from huggingface_hub import login
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from pebblo.log import get_logger
from pebblo.topic_classifier.config import (
    CLASSIFIER_PATH,
    MODEL_REVISION,
    TOKENIZER_PATH,
    TOPIC_CONFIDENCE_SCORE,
    TOPIC_MIN_TEXT_LENGTH,
    TOPICS_TO_EXCLUDE,
)
from pebblo.topic_classifier.enums.constants import topic_display_names
from pebblo.utils import get_confidence_score_label

logger = get_logger(__name__)


class TopicClassifier:
    """
    Class for topic classification
    """

    def __init__(self):
        # Use os.environ.get() to retrieve the value of the environment variable

        huggingface_token = os.environ.get("HF_TOKEN")

        # Check if the environment variable exists
        if huggingface_token is not None:
            login(token=huggingface_token)

        # Load the model and tokenizer from the specified paths and revision
        _tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_PATH, revision=MODEL_REVISION
        )
        _model = AutoModelForSequenceClassification.from_pretrained(
            CLASSIFIER_PATH, revision=MODEL_REVISION
        )
        self.classifier = pipeline(
            "text-classification",
            model=_model,
            tokenizer=_tokenizer,
            truncation=True,
            max_length=512,
            return_all_scores=True,
        )

    def predict(self, input_text):
        """
        Perform topic classification on the input data.
        """
        try:
            # Check if the input text meets the minimum length requirement
            if len(input_text) <= TOPIC_MIN_TEXT_LENGTH:
                logger.debug(
                    f"Text length is below {TOPIC_MIN_TEXT_LENGTH} characters. "
                    f"Classification not performed."
                )
                return {}, 0, {}

            topic_model_response = self.classifier(input_text)
            topics, total_count, topic_details = self._get_topics(topic_model_response)
            logger.debug(f"Topics: {topics}")
            return topics, total_count, topic_details
        except Exception as e:
            logger.error(f"Error in topic_classifier. Exception: {e}")
            return {}, 0, {}

    @staticmethod
    def _get_topics(topic_model_response):
        topic_model_response = topic_model_response[0]
        topics = dict()
        for topic in topic_model_response:
            topic_label = topic["label"]
            if topic_label in TOPICS_TO_EXCLUDE:
                continue
            if topic["score"] < float(TOPIC_CONFIDENCE_SCORE):
                continue
            if topic_label in topic_display_names.keys():
                mapped_topic = topic_display_names[topic_label]
                topics[mapped_topic] = topic["score"]

        final_topic = {}
        topic_details = {}
        if len(topics) > 0:
            most_possible_advice = max(topics, key=lambda t: topics[t])
            final_topic = {most_possible_advice: 1}
            topic_details = {
                most_possible_advice: [
                    {
                        "confidence_score": get_confidence_score_label(
                            (topics[most_possible_advice])
                        )
                    }
                ]
            }
        return final_topic, len(final_topic.keys()), topic_details
