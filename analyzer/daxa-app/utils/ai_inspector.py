# Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.

import re
from os import environ
from dotenv import load_dotenv
from sagemaker.huggingface.model import HuggingFacePredictor
from enums.inspector_constants import ConfidenceScore, InspectorConfig, Entities, Topics
from enums.regex_pattern import regex_secrets_patterns
from libs.logger import logger


class Inspector:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.topic_classifier_endpoint = environ.get("TOPIC_CLASSIFIER_ENDPOINT")
        self.ner_classifier_endpoint = environ.get("NER_CLASSIFIER_ENDPOINT")
        self.topic_model = HuggingFacePredictor(endpoint_name=self.topic_classifier_endpoint)
        self.ner_model = HuggingFacePredictor(endpoint_name=self.ner_classifier_endpoint)
        self._max_len_limit = InspectorConfig.input_max_len.value


    def topic_classifier(self, data):
        """
        Perform classification on the input data and return a dictionary with the count of each item and the total count.
        Parameters:
            - input_data (dict): A dictionary containing input data for classification.
        Returns:
            dict: containing the topic Name as key and its count as value.
            total_count: Total count of topics.
        Example:{
                'MEDICAL_ADVICE': 1, # topic_name : Count of occurrence of topic.
                'LEGAL_ADVICE': 1
            },
            total_count: 2 # total count of occurrence of all topics.
        """
        restricted_topics = {}
        total_count = 0
        try:
            logger.debug("Topic Classifier Started.")
            input_data = " ".join(str(data).split()[:self._max_len_limit])
            data_input = {"inputs": input_data}
            logger.debug(f"Data Input : {data_input}")
            # The endpoint responds [[]], one list per input string.
            # we are using first list as we are passing only one string as input.
            topic_model_response = self.topic_model.predict(data_input)
            if len(topic_model_response) == 0:
                return restricted_topics, total_count
            restricted_topics, total_count = self._get_restricted_topics(topic_model_response[0])
            logger.debug(f"Topic Response: {topic_model_response}")
            logger.info(f"Topic Classifier Finished. {restricted_topics}")
            return restricted_topics, total_count
        except Exception as e:
            logger.error(f"Topic Classifier Failed. Exception: {e}")
            return restricted_topics, total_count

    def ner_classifier(self, data):
        """
                Perform classification on the input data and return a dictionary with the count of each entity group.
                Parameters:
                    - input_data (dict): A dictionary containing input data for classification.
                Returns:
                    dict: containing the entity group Name as key and its count as value.
                    total_count: Total count of entity groups.
                Example:{
                        'Person':2, # EntityGroup: Count of occurrence of entity group
                        'Credit Card Number: 1
                    },
                    total_count: 3 # Total Count of All Entity group Occurrences
        """
        restricted_entities = {}
        total_count = 0
        try:
            logger.debug("NER Classifier Started.")
            input_data = " ".join(str(data).split()[:self._max_len_limit])
            data_input = {"inputs": input_data}
            logger.debug(f"Data Input: {data_input}")
            logger.debug(self.ner_classifier_endpoint)
            ner_model_response = self.ner_model.predict(data_input)
            logger.debug(f"NER Response: {ner_model_response}")
            restricted_entities, total_count = self._get_restricted_entities(ner_model_response)

            logger.info(f"NER Classifier Finished. {restricted_entities}")
            return restricted_entities, total_count
        except Exception as e:
            logger.error(f"NER Classifier Failed, Exception: {e}")
            return restricted_entities, total_count

    def secret_classifier(self, data):
        """
            Find regex patterns in the given input data.

            Parameters:
            - input_data (str): The input string to search for regex patterns.

            Returns:
            dict: A dictionary containing key associated with regex patterns and their counts in the input data.
            Example:
            {
                'AWS API ID': 3, # SecretKey: Count of Occurrences of secret key
                'AWS API Secret': 1
            },
            total_count: 4 # total count of all SecretKeys Occurrences
            """
        secrets = dict()
        total_count = 0
        data = str(data)
        try:
            logger.debug("Secret Classifier Started.")
            # Loop through a collection of regex patterns, checking each pattern against the input data.
            for secret_key in regex_secrets_patterns.keys():
                try:
                    matches: list = re.findall(regex_secrets_patterns[secret_key], data)
                    if len(matches):
                        secrets[secret_key] = secrets.get(secret_key, 0) + len(matches)
                        total_count += len(matches)
                except Exception as e:
                    logger.debug(f"Failed In Checking Regex: {secret_key}, Exception: {e}")
                    continue
            return secrets, total_count
        except Exception as e:
            logger.error(f"Secret Classifier Failed, Exception: {e}")
            return secrets, total_count

    def _get_restricted_topics(self, topic_model_response):
        restricted_topics = dict()
        for topic in topic_model_response:
            if topic["score"] < float(ConfidenceScore.Topic.value):
                continue

            if topic["label"] in Topics.__members__:
                mapped_entity = Topics[topic["label"]].value
                restricted_topics[mapped_entity] = topic["score"]

        final_topic = {}
        if len(restricted_topics) > 0:
            most_possible_advice = max(restricted_topics, key=restricted_topics.get)
            final_topic = {most_possible_advice: 1}
        return final_topic, len(final_topic.keys())

    def _get_restricted_entities(self, ner_model_response):
        restricted_entity_groups = dict()
        total_count = 0
        for entity in ner_model_response:
            if entity["score"] < float(ConfidenceScore.NER.value):
                continue

            if entity["entity_group"] in Entities.__members__:
                mapped_entity = Entities[entity["entity_group"]].value
                restricted_entity_groups[mapped_entity] = restricted_entity_groups.get(mapped_entity, 0) + 1
                total_count += 1

        return restricted_entity_groups, total_count
