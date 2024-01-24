import os

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

from pebblo.topic_classifier.config import TOPIC_CONFIDENCE_SCORE, TOKENIZER_PATH, CLASSIFIER_PATH
from pebblo.topic_classifier.enums.constants import topic_display_names
from pebblo.topic_classifier.libs.logger import logger

# Use os.environ.get() to retrieve the value of the environment variable
huggingface_token = os.environ.get("HF_TOKEN")

# Check if the environment variable exists
if huggingface_token is not None:
    from huggingface_hub import login

    login(token=huggingface_token)


class TopicClassifier:
    """
    Class for topic classification
    """

    def __init__(self):
        _tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(CLASSIFIER_PATH)
        self.classifier = pipeline("text-classification", model=_model, tokenizer=_tokenizer,
                                   truncation=True, max_length=512, return_all_scores=True)

    def predict(self, input_text):
        """
        Perform topic classification on the input data.
        """
        try:
            topic_model_response = self.classifier(input_text)
            topics, total_count = self._get_topics(topic_model_response)
            logger.debug(f"Topics: {topics}")
            return topics, total_count
        except Exception as e:
            logger.error(f"Error in topic_classifier. Exception: {e}")
            return {}, 0

    @staticmethod
    def _get_topics(topic_model_response):
        logger.debug(f"Topics model response: {topic_model_response}")
        topic_model_response = topic_model_response[0]
        topics = dict()
        for topic in topic_model_response:
            topic_label = topic["label"]
            if topic["score"] < float(TOPIC_CONFIDENCE_SCORE):
                continue
            if topic_label in topic_display_names.keys():
                mapped_topic = topic_display_names[topic_label]
                topics[mapped_topic] = topic["score"]

        final_topic = {}
        if len(topics) > 0:
            most_possible_advice = max(topics, key=topics.get)
            final_topic = {most_possible_advice: 1}
        return final_topic, len(final_topic.keys())


