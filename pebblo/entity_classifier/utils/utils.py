"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""

from presidio_analyzer import Pattern, PatternRecognizer, RecognizerRegistry

from pebblo.entity_classifier.utils.config import (
    ConfidenceScore,
    Entities,
    SecretEntities,
    secret_entities_context_mapping,
)
from pebblo.entity_classifier.utils.regex_pattern import regex_secrets_patterns


def get_entities(entities_list, response):
    entity_groups = dict()
    total_count = 0
    for entity in response:
        if entity["entity_type"] in entities_list:
            if entity["entity_type"] in Entities.__members__:
                mapped_entity = Entities[entity["entity_type"]].value
            elif entity["entity_type"] in SecretEntities.__members__:
                mapped_entity = SecretEntities[entity["entity_type"]].value
            entity_data = {
                "location": entity["location"],
                "confidence_score": entity["confidence_score"],
            }
            if mapped_entity in entity_groups.keys():
                entity_groups[mapped_entity].append(entity_data)
            else:
                entity_groups[mapped_entity] = [entity_data]
            total_count += 1

    return entity_groups, total_count


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
