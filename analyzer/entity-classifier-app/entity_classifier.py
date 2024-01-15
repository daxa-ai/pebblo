from enum import Enum

# from stdlib.log import get_logger
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# logger = get_logger("rag.analyzer.entity_classifier")


class Entities(Enum):
    # PII
    US_SSN = "US SSN"
    US_PASSPORT = "US Passport number"
    US_DRIVER_LICENSE = "US Drivers License"

    # Financial
    CREDIT_CARD = "Credit card number"
    US_BANK_NUMBER = "US Bank Account Number"
    IBAN_CODE = "IBAN code"
    US_ITIN = "US ITIN"


class EntityClassifier:
    def __init__(self, input_text):
        self.input_text = input_text
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def presidio_entity_classifier(self):
        """
        Perform classification on the input data and return a dictionary with the count of each entity group.
        Parameters:
            - input_data (dict): A dictionary containing input data for classification.
        Returns:
            dict: containing the entity group Name as key and its count as value.
            total_count: Total count of entity groups.
        Example:{
                "Person":2, # EntityGroup: Count of occurrence of entity group
                "Credit Card Number": 1
            },
            total_count: 3 # Total Count of All Entity group Occurrences
        """
        restricted_entities = {}
        total_count = 0
        try:
            # logger.info("Presidio Entity Classifier Started.")
            # logger.info(f"Data Input: {self.input_text}")
            analyzer_results = self.analyzer.analyze(text=self.input_text, language='en')
            anonymized_text = self.anonymizer.anonymize(text=self.input_text, analyzer_results=analyzer_results)
            presidio_response = anonymized_text.items
            # logger.info(f"Presidio Entity Classifier Response: {presidio_response}")
            restricted_entities, total_count = self._get_restricted_entities(presidio_response)

            # logger.info(f"Presidio Entity Classifier Finished. {restricted_entities}")
            # logger.info(f"Entity Total count. {total_count}")
            return restricted_entities, total_count
        except Exception as e:
            # logger.error(f"Presidio Entity Classifier Failed, Exception: {e}")
            return restricted_entities, total_count

    @staticmethod
    def _get_restricted_entities(presidio_response):
        restricted_entity_groups = dict()
        total_count = 0
        for entity in presidio_response:
            if entity.entity_type in Entities.__members__:
                mapped_entity = Entities[entity.entity_type].value
                restricted_entity_groups[mapped_entity] = restricted_entity_groups.get(mapped_entity, 0) + 1
                total_count += 1

        return restricted_entity_groups, total_count
