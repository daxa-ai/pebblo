"""
Copyright (c) 2024 Cloud Defense, Inc. All rights reserved.
"""
from presidio_analyzer import Pattern, PatternRecognizer

from pebblo.entity_classifier.utils.config import SecretEntities, ConfidenceScore
from pebblo.entity_classifier.utils.regex_pattern import regex_secrets_patterns


def get_entities(entities_enum, response):
    entity_groups = dict()
    total_count = 0
    for entity in response:
        if entity.entity_type in entities_enum.__members__:
            mapped_entity = entities_enum[entity.entity_type].value
            entity_groups[mapped_entity] = entity_groups.get(mapped_entity, 0) + 1
            total_count += 1

    return entity_groups, total_count


def add_custom_regex_analyzer_registry():
    regex_recognizer = []
    # Creating custom regex recognizer
    for entity, regex_pattern in regex_secrets_patterns.items():
        pattern = [
            Pattern(
                name=SecretEntities(entity).value,
                regex=regex_pattern,
                score=float(ConfidenceScore.Entity.value)
            ),
        ]

        recognizer = PatternRecognizer(
            supported_entity=SecretEntities(entity).name,
            name=f"{'_'.join(entity.split(' '))}_recognizer",
            patterns=pattern
        )
        regex_recognizer.append(recognizer)

    return regex_recognizer
