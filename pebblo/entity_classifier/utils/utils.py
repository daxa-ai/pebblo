"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""

from presidio_analyzer import Pattern, PatternRecognizer, RecognizerRegistry

from pebblo.entity_classifier.utils.config import (
    ConfidenceScore,
    Entities,
    SecretEntities,
    entity_group_conf_mapping,
    secret_entities_context_mapping,
)
from pebblo.entity_classifier.utils.regex_pattern import regex_secrets_patterns
from pebblo.utils import get_confidence_score_label


def get_entities(entities_list, response):
    entity_groups: dict = dict()
    entity_details: dict = dict()

    mapped_entity = None
    total_count = 0
    for entity in response:
        if entity["entity_type"] in entities_list:
            if entity["entity_type"] in Entities.__members__:
                mapped_entity = Entities[entity["entity_type"]].value
            elif entity["entity_type"] in SecretEntities.__members__:
                mapped_entity = SecretEntities[entity["entity_type"]].value
            entity_groups[mapped_entity] = entity_groups.get(mapped_entity, 0) + 1
            entity_data = {
                "location": entity["location"],
                "confidence_score": get_confidence_score_label(
                    entity["confidence_score"]
                ),
                "entity_group": entity_group_conf_mapping[mapped_entity][1],
            }
            if mapped_entity in entity_details.keys():
                entity_details[mapped_entity].append(entity_data)
            else:
                entity_details[mapped_entity] = [entity_data]
            total_count += 1

    return entity_groups, entity_details, total_count


def add_custom_regex_analyzer_registry():
    """
    Using context word enhancer
    :return: Recognizer Registry with patterns and contexts
    """
    recognizer_registry = RecognizerRegistry()

    # Creating custom regex recognizer
    for entity, regex_pattern in regex_secrets_patterns.items():
        # Define regex pattern
        pattern = [
            Pattern(
                name=SecretEntities(entity).value,
                regex=regex_pattern,
                score=float(ConfidenceScore.EntityMinScore.value),
            ),
        ]

        # Define recognizer with the defined pattern
        recognizer = PatternRecognizer(
            supported_entity=SecretEntities(entity).name,
            name=f"{'_'.join(entity.split(' '))}_recognizer",
            patterns=pattern,
            context=secret_entities_context_mapping[SecretEntities(entity).value],
        )
        recognizer_registry.add_recognizer(recognizer)

    return recognizer_registry
