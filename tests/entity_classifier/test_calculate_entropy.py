from pebblo.entity_classifier.custom_analyzer.calculate_entropy import (
    is_high_entropy_secret,
)


def test_is_high_entropy_secret():
    # Test for string with a single character (e.g., "a")
    assert is_high_entropy_secret("aaaaaaa") is False
    assert is_high_entropy_secret("a1b2c3d4e5ase456/AEQ=") is True
