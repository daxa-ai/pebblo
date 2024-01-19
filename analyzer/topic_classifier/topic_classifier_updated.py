import os
from enum import Enum
from operator import itemgetter

import joblib
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

from analyzer.topic_classifier.libs.logger import logger

# Use os.environ.get() to retrieve the value of the environment variable
huggingface_token = os.environ.get("HF_TOKEN")

# Check if the environment variable exists
if huggingface_token is not None:
    logger.debug(f"HF_TOKEN is: {huggingface_token}")
    from huggingface_hub import login

    login(token=huggingface_token)
else:
    logger.warning("HF_TOKEN is not set.")


# TODO: Refactor following code
class Topics(Enum):
    """
    Enumeration of all possible topics
    """
    MEDICAL_ADVICE = "Medical Advice"
    HARMFUL_ADVICE = "Harmful Advice"


TOPIC_CONFIDENCE_SCORE = 0.60

# Paths
MODEL_PATH = 'daxa-ai/Daxa-Classifier-Bert'  # Path to your saved model
LABEL_ENCODER_PATH = 'daxa-ai/Daxa-Classifier-Bert'  # Path to your saved label encoder
TOKENIZER_PATH = 'distilbert-base-uncased'


class TextClassifier:
    """
    Class for topic classification
    """

    def __init__(self):
        self.model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(TOKENIZER_PATH)

    def predict(self, text):
        """
        Perform topic classification on the input data and predict the topics
        """
        try:
            inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)

            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
            probabilities_np = probabilities.numpy()
            sorted_probs = self.zip_and_sort(self.label_encoder.classes_, probabilities_np)
            # highest_prob_label = self.label_encoder.classes_[np.argmax(probabilities_np)]
            # highest_prob = np.max(probabilities_np)
            # return sorted_probs, highest_prob_label, highest_prob
            # TODO: Finalize the return value format
            return self._get_topics(sorted_probs)
        except Exception as e:
            print(f"Error while performing topic classification. Reason: {e}")
            return []

    @staticmethod
    def _get_topics(topic_model_response):
        topics = dict()
        for topic in topic_model_response:
            if topic["score"] < float(TOPIC_CONFIDENCE_SCORE):
                continue
            if topic["label"] in Topics.__members__:
                mapped_topic = Topics[topic["label"]].value
                topics[mapped_topic] = topic["score"]
        final_topic = {}
        if len(topics) > 0:
            most_possible_advice = max(topics, key=topics.get)
            final_topic = {most_possible_advice: 1}
        return final_topic, len(final_topic.keys())

    @staticmethod
    def zip_and_sort(labels, scores):
        """
        Zip and sort the labels by scores
        :param labels: labels
        :param scores: scores
        :return: list of topics sorted by scores
        """
        pairs = zip(labels, scores)
        result = [{"label": key, "score": value} for key, value in pairs]
        result = sorted(result, key=itemgetter("score"), reverse=True)
        return result


if __name__ == "__main__":
    classifier = TextClassifier()
    input_text = "My name is Wolfgang and I live in Berlin"
    classifier_results = classifier.predict(input_text)
    print(classifier_results)
