import math


def calculate_entropy(data: str) -> float:
    """
    Calculate the Shannon entropy of a given string.

    Entropy is a measure of randomness or uncertainty in a dataset.
    The higher the entropy, the more unpredictable the data is.

    Args:
        data (str): The input string for which entropy is to be calculated.

    Returns:
        float: The entropy value of the input string. If the string is empty, returns 0.
    """
    if not data:
        return 0.0  # Return 0 entropy for empty input

    entropy: float = 0.0  # Initialize entropy value
    # Calculate the probability of each character in the string
    for char in set(data):
        p_x: float = float(data.count(char)) / len(data)
        # Calculate entropy using the formula: -sum(p_x * log2(p_x))
        entropy -= p_x * math.log2(p_x)

    return entropy  # Return the calculated entropy


def is_high_entropy_secret(value: str) -> bool:
    """
    Determine if a given string is a high-entropy secret.

    This function uses the Shannon entropy to assess whether a string has
    high randomness, which is a common characteristic of sensitive data like keys.

    Args:
        value (str): The input string to be evaluated.

    Returns:
        bool: True if the string has high entropy (>= 4), indicating it may be a secret.
              False otherwise.
    """
    entropy: float = calculate_entropy(
        value
    )  # Calculate the entropy of the input string
    if entropy >= 4.0:  # Check if the entropy meets or exceeds the threshold of 4
        return True  # High entropy detected, return True
    return False  # Entropy below the threshold, return False
