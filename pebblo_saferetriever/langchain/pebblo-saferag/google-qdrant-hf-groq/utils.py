import textwrap
from typing import List, Optional


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
