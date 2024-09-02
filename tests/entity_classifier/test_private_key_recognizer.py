from pebblo.entity_classifier.custom_analyzer.private_key_analyzer import (
    PrivateKeyRecognizer,
)


def test_private_key_recognizer_no_match():
    # Test case where there is no private key in the text
    text = "This is a test string with no private key."
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 0

    # Test case with a string that looks like a private key but fails entropy check
    text = "-----BEGIN PRIVATE KEY-----\nAAAAAAAABBBBBBBB\n-----END PRIVATE KEY-----\n"
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 0


def test_private_key_recognizer__matche():
    # Test case with multiple private keys in the text
    text = """

        "{\n"
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqh\\n-----END PRIVATE KEY-----\\n\",\n"
        "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEj8K3X9sL7WzM2pY5qT1G6oV4rF8bN0dJ2cH7wB9mL3vP6nR1uQ8sT4zX7eD2oA5gK3pJ9tM1rC6yV4qW2bF7nH0sL5o=\\n-----END PRIVATE KEY-----\\n\",\n\n"
        "}\n\n"

    """
    recognizer = PrivateKeyRecognizer()
    results = recognizer.analyze(text, entities=["PRIVATE_KEY"])

    assert len(results) == 1
