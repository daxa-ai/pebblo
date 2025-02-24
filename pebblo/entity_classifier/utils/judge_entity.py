import ast
import logging

from pebblo.entity_classifier.utils.prompt_lib import get_judge_prompt

logger = logging.getLogger()


def process_group(group, text, text_generation_obj):
    """
    Process a group of overlapping entities. Replace this with your actual processing logic.

    Args:
    group (list): List of overlapping entities.
    """
    group_dict = []
    for g in group:
        group_dict.append(
            {"entity_type": g.entity_type, "entity_value": text[g.start : g.end]}
        )
    final_prompt = get_judge_prompt(text, group_dict)
    judgement = text_generation_obj.generate(final_prompt)
    judgement = ast.literal_eval(judgement)
    if isinstance(judgement, list):
        judge_dict = {}
        for judge in judgement:
            judge_dict.update(judge)
        judgement = judge_dict

    correct_judgement = [
        key for key, value in judgement.items() if value.lower() == "correct"
    ]
    filtered_group = [
        entity for entity in group if entity.entity_type in correct_judgement
    ]
    return filtered_group


def judge_results(text, grouped_entities, text_generation_obj):
    # Group overlapping entities
    final_entities = []
    # Process each group
    for group in grouped_entities:
        if len(group) > 1:
            filtered_grp = process_group(group, text, text_generation_obj)
            for ent in filtered_grp:
                final_entities.extend(filtered_grp)
        else:
            final_entities.extend(group)
    return final_entities
