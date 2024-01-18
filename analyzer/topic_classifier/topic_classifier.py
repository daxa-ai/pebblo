from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

from analyzer.topic_classifier.config import TOPIC_CONFIDENCE_SCORE, TOKENIZER_PATH, CLASSIFIER_PATH
from analyzer.topic_classifier.enums.enums import Topics


class TopicClassifier:
    """
    Class for topic classification
    """

    def __init__(self, input_text):
        _tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(CLASSIFIER_PATH)
        self.classifier = pipeline("text-classification", model=_model, tokenizer=_tokenizer, return_all_scores=True)
        self.input_text = input_text

    def topic_classifier(self):
        """
        Perform topic classification on the input data.
        """
        restricted_topics = {}
        total_count = 0
        try:
            classifier_results = self.classifier(self.input_text)
            restricted_topics, total_count = self._get_restricted_topics(classifier_results)
            return restricted_topics, total_count
        except Exception as e:
            return restricted_topics, total_count

    def _get_restricted_topics(self, topic_model_response):
        print(topic_model_response)
        topic_model_response = topic_model_response[0]
        restricted_topics = dict()
        for topic in topic_model_response:
            if topic["score"] < float(TOPIC_CONFIDENCE_SCORE):
                continue
            if topic["label"] in Topics.__members__:
                mapped_topic = Topics[topic["label"]].value
                restricted_topics[mapped_topic] = topic["score"]
        final_topic = {}
        if len(restricted_topics) > 0:
            most_possible_advice = max(restricted_topics, key=restricted_topics.get)
            final_topic = {most_possible_advice: 1}
        return final_topic, len(final_topic.keys())
