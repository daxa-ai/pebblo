import json
from typing import List, Optional

from presidio_analyzer import (
    EntityRecognizer,
    Pattern,
    RecognizerResult,
)
from presidio_analyzer.nlp_engine import NlpArtifacts

from pebblo.entity_classifier.utils.prompt_lib import get_entity_detection_prompt
from pebblo.entity_classifier.utils.result_validation import extract_entity_info
from pebblo.log import get_logger
from pebblo.text_generation.text_generation import TextGeneration

logger = get_logger(__name__)


ENTITY_LABELS_UNIQUE = {
    "iban": "IBAN_CODE",
    "ssn": "US_SSN",
    "passport_number": "US_PASSPORT",
    "driver_license_number": "US_DRIVER_LICENSE",
    "credit_card_number": "CREDIT_CARD",
    "name": "LLM_PERSON",
    "company": "LLM_ORGANIZATION",
    "street_address": "STREET_ADDRESS",
    "email": "EMAIL_ADDRESS",
    "phone_number": "PHONE_NUMBER",
    "date_of_birth": "DATE_OF_BIRTH",
    "bank_routing_number": "ROUTING_NUMBER",
    "bank_account_number": "US_BANK_NUMBER",
    "swift_bic_code": "SWIFT_CODE",
    "api_key": "API_KEY",
    "private_keys": "PRIVATE_KEY",
    "itin": "US_ITIN",
    "ip_address": "IP_ADDRESS",
    "bban": "BBAN_CODE",
}


class LLMRecognizer(EntityRecognizer):
    """
    Custom recognizer that uses an external LLM model for entity detection.
    """

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = list(ENTITY_LABELS_UNIQUE.values()),
    ):
        super().__init__(
            supported_entities=supported_entity,
            context=context,
            supported_language=supported_language,
        )
        self.text_gen_obj = TextGeneration()

    def analyze(
        self,
        text,
        entities: List[str] = [],
        nlp_artifacts: Optional[NlpArtifacts] = None,
        regex_flags: Optional[int] = None,
    ):
        """
        Override the analyze method to detect entities using the LLM model.
        :param text: The text to analyze.
        :param entities: The list of entity types to detect.
        :param nlp_artifacts: Optional NLP pipeline artifacts (unused in this recognizer).
        :return: List of RecognizerResult objects.
        """

        # Calling the llm_analyzer function you provided
        detected_entities = self.llm_analyzer(text)
        # Create a list of RecognizerResult objects based on detected entities
        results = []
        for entity in detected_entities:
            entity_det = entity.get("label")
            if entity_det:
                entity_type = ENTITY_LABELS_UNIQUE.get(entity_det)
                start = entity.get("start")
                end = entity.get("end")
                score = entity.get(
                    "confidence", 0.8
                )  # default score is 1.0 if not provided

            if abs(end - start) > 2:
                # Append to results as a RecognizerResult object
                results.append(RecognizerResult(entity_type, start, end, score))
        return results

    def llm_analyzer(self, text):
        """
        Your custom LLM entity detection logic.
        """
        messages = get_entity_detection_prompt(text)

        # Assuming text_gen_obj is already defined and initialized elsewhere
        entities = self.text_gen_obj.generate(messages)
        entities = json.loads(entities)
        if isinstance(entities, dict):
            entities = [entities]

        # Extract entity information from the detected entities
        entities = extract_entity_info(entities, text)
        return entities
