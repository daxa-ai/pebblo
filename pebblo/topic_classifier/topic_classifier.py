"""
Module for topic classification using Pebblo and Hugging Face.
Defines the TopicClassifier class with methods for predicting topics and extracting them from the model's response.
"""

import os
import re

from huggingface_hub import login
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from pebblo.log import get_logger
from pebblo.text_generation.text_generation import TextGeneration
from pebblo.topic_classifier.config import (
    CLASSIFIER_PATH,
    MODEL_REVISION,
    TOKENIZER_PATH,
    TOPIC_CLASS_REGEX_STR,
    TOPIC_CONFIDENCE_SCORE,
    TOPIC_MIN_TEXT_LENGTH,
    TOPICS_TO_EXCLUDE,
    USE_LLM,
)
from pebblo.topic_classifier.enums.constants import topic_display_names
from pebblo.topic_classifier.llm_classification_prompt import (
    SYSTEM_PROMPT_V2,
    USER_PROMPT,
)
from pebblo.utils import ConfidenceScoreLabel, get_confidence_score_label

logger = get_logger(__name__)


class TopicClassifier:
    """
    Class for topic classification
    """

    def __init__(self):
        # Use os.environ.get() to retrieve the value of the environment variable
        self.use_llm = USE_LLM
        self.txt_gen = TextGeneration()
        huggingface_token = os.environ.get("HF_TOKEN")

        # Check if the environment variable exists
        if huggingface_token is not None:
            login(token=huggingface_token)
        if self.use_llm is False:
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

    def clean_class_name(self, label):
        match = re.search(TOPIC_CLASS_REGEX_STR, label, re.IGNORECASE)
        return match.group(0) if match else None

    def predict(self, input_text):
        """
        Perform topic classification on the input data.
        """
        try:
            # Check if the input text meets the minimum length requirement
            if len(input_text.split()) <= TOPIC_MIN_TEXT_LENGTH:
                logger.debug(
                    f"Text length is below {TOPIC_MIN_TEXT_LENGTH} characters. "
                    f"Classification not performed."
                )
                return {}, 0, {}

            if self.use_llm is False:
                topic_model_response = self.classifier(input_text)
                topics, total_count, topic_details = self._get_topics(
                    topic_model_response
                )
                logger.debug(f"Topics: {topics}")
                return topics, total_count, topic_details
            else:
                message = self.get_message(input_text)

                op_classes = self.txt_gen.generate_classification(message)
                if isinstance(op_classes, str):
                    op_classes = self.clean_class_name(op_classes)
                    if op_classes is None or op_classes.lower() == "other":
                        return {}, 0, {}
                    else:
                        return (
                            {op_classes.upper(): 1},
                            1,
                            {
                                op_classes.upper(): [
                                    {
                                        "confidence_score": ConfidenceScoreLabel.MEDIUM.value
                                    }
                                ]
                            },
                        )
                elif isinstance(op_classes, list):
                    op_dict = {}
                    op_conf = {}
                    cnt_classes = 0
                    for op_cls in op_classes:
                        op_cls = self.clean_class_name(op_cls)
                        if op_cls is not None and op_cls.lower() != "other":
                            cnt_classes += 1
                            op_dict[op_cls.upper()] = op_dict.get(op_cls.upper(), 0) + 1
                            if op_cls not in op_conf.keys():
                                op_conf[op_cls.upper()] = [
                                    {
                                        "confidence_score": ConfidenceScoreLabel.MEDIUM.value
                                    }
                                ]
                            else:
                                op_conf[op_cls.upper()].append(
                                    {
                                        "confidence_score": ConfidenceScoreLabel.MEDIUM.value
                                    }
                                )
                    return op_dict, cnt_classes, op_conf
                else:
                    return {}, 0, {}
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

    def get_message(self, text):
        user_pr = USER_PROMPT.format(text=text)
        messages = [
            # This line is commented because Gemma does not support system role
            # {"role": "system", "content": SYSTEM_PROMPT_V2},
            {"role": "user", "content": SYSTEM_PROMPT_V2 + " " + user_pr},
        ]
        return messages
