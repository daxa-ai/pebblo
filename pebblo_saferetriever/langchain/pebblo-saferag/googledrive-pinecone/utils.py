import textwrap
from typing import List, Optional


def describe_pebblo_semantic_stats(documents: list) -> None:
    """
    Describe the semantic stats of the documents
    """
    unique_identities = set()
    unique_topics = set()
    unique_entities = set()

    for doc in documents:
        unique_identities.update(doc.metadata.get("authorized_identities", []))
        unique_topics.update(doc.metadata.get("pebblo_semantic_topics", []))
        unique_entities.update(doc.metadata.get("pebblo_semantic_entities", []))

    print("\nIndentity and Semantic Stats:")
    print(f"Authorized Identities: {list(unique_identities)}")
    print(f"Semantic Topics: {list(unique_topics)}")
    print(f"Semantic Entities: {list(unique_entities)}")
    print("\n")


def format_text(text: str, width: int = 120):
    """
    Format the text to a given width
    """
    formatted_text = textwrap.fill(
        text,
        width=width,
        fix_sentence_endings=True,
        replace_whitespace=False,
    )
    return formatted_text


def get_input_as_list(prompt_text: str) -> Optional[List[str]]:
    """
    Get user input as list
    """
    user_input = input(prompt_text)
    if user_input:
        return [item.strip() for item in user_input.split(",") if item.strip()]
    else:
        return None
