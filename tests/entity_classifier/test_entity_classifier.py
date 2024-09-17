import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.mock_response import (
    mock_input_text1_anonymize_snippet_true,
    mock_input_text2_anonymize_snippet_true,
)
from tests.entity_classifier.test_data import input_text1, input_text2, negative_data


class TestAnonymizerResult:
    def __init__(self, entity_type):
        self.entity_type = entity_type


@pytest.fixture
def entity_classifier():
    """
    Create an instance of the EntityClassifier class
    """
    return EntityClassifier()


def test_entity_classifier_init() -> None:
    """
    Initiated Entity Classifier
    """
    _ = EntityClassifier()


def test_entity_classifier_and_anonymizer1(entity_classifier):
    """
    UT for presidio_entity_classifier_and_anonymizer function with input_text1
    """
    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1)
    assert entities == {
        "github-token": 1,
        "aws-access-key": 1,
        "us-itin": 1,
        "us-ssn": 1,
    }
    assert total_count == 4
    assert anonymized_text == input_text1
    assert entity_details == {
        "us-ssn": [
            {
                "location": "17_28",
                "confidence_score": "HIGH",
                "entity_group": "pii-identification",
            }
        ],
        "us-itin": [
            {
                "location": "42_53",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "aws-access-key": [
            {
                "location": "77_97",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "120_210",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text1, True)
    assert entities == {
        "github-token": 1,
        "aws-access-key": 1,
        "us-itin": 1,
        "us-ssn": 1,
    }
    assert total_count == 4
    assert anonymized_text == mock_input_text1_anonymize_snippet_true
    assert entity_details == {
        "us-ssn": [
            {
                "location": "17_31",
                "confidence_score": "HIGH",
                "entity_group": "pii-identification",
            }
        ],
        "us-itin": [
            {
                "location": "45_60",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "aws-access-key": [
            {
                "location": "84_106",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "129_149",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
    }


def test_entity_classifier_and_anonymizer2(entity_classifier):
    """
    UT for presidio_entity_classifier_and_anonymizer function with input_text2
    """
    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(input_text2)
    assert entities == {
        "us-ssn": 1,
        "us-drivers-license": 1,
        "us-bank-account-number": 1,
        "credit-card-number": 1,
        "iban-code": 1,
        "us-itin": 1,
        "client-secret": 3,
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "github-token": 1,
        "slack-token": 2,
        "ip-address": 1,
    }
    assert total_count == 15
    assert anonymized_text == input_text2
    assert entity_details == {
        "us-ssn": [
            {
                "location": "1178_1189",
                "confidence_score": "HIGH",
                "entity_group": "pii-identification",
            }
        ],
        "us-drivers-license": [
            {
                "location": "1257_1265",
                "confidence_score": "MEDIUM",
                "entity_group": "pii-identification",
            }
        ],
        "us-bank-account-number": [
            {
                "location": "1299_1316",
                "confidence_score": "MEDIUM",
                "entity_group": "pii-financial",
            }
        ],
        "credit-card-number": [
            {
                "location": "1361_1376",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "iban-code": [
            {
                "location": "1398_1426",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "us-itin": [
            {
                "location": "1440_1451",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "client-secret": [
            {
                "location": "1475_1511",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1841_1877",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "2058_2094",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "aws-access-key": [
            {
                "location": "1532_1552",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "aws-secret-key": [
            {
                "location": "1573_1614",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "1631_1721",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "slack-token": [
            {
                "location": "1795_1818",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1892_1949",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "ip-address": [
            {
                "location": "2023_2034",
                "confidence_score": "HIGH",
                "entity_group": "pii-network",
            }
        ],
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        input_text2, anonymize_snippets=True
    )
    assert entities == {
        "us-ssn": 1,
        "us-drivers-license": 1,
        "us-bank-account-number": 1,
        "credit-card-number": 1,
        "iban-code": 1,
        "us-itin": 1,
        "client-secret": 3,
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "github-token": 1,
        "slack-token": 2,
        "ip-address": 1,
    }
    assert total_count == 15
    assert anonymized_text == mock_input_text2_anonymize_snippet_true
    assert entity_details == {
        "us-ssn": [
            {
                "location": "1178_1192",
                "confidence_score": "HIGH",
                "entity_group": "pii-identification",
            }
        ],
        "us-drivers-license": [
            {
                "location": "1260_1285",
                "confidence_score": "MEDIUM",
                "entity_group": "pii-identification",
            }
        ],
        "us-bank-account-number": [
            {
                "location": "1319_1341",
                "confidence_score": "MEDIUM",
                "entity_group": "pii-financial",
            }
        ],
        "credit-card-number": [
            {
                "location": "1386_1405",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "iban-code": [
            {
                "location": "1427_1444",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "us-itin": [
            {
                "location": "1458_1473",
                "confidence_score": "HIGH",
                "entity_group": "pii-financial",
            }
        ],
        "client-secret": [
            {
                "location": "1497_1518",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1757_1778",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1928_1949",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "aws-access-key": [
            {
                "location": "1539_1561",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "aws-secret-key": [
            {
                "location": "1582_1604",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "1621_1641",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "slack-token": [
            {
                "location": "1715_1734",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1793_1812",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "ip-address": [
            {
                "location": "1886_1904",
                "confidence_score": "HIGH",
                "entity_group": "pii-network",
            }
        ],
    }


def test_entity_classifier_and_anonymizer_negative_data(entity_classifier):
    """
    UT for presidio_entity_classifier_and_anonymizer function with negative_data
    """
    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(negative_data)
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(
        negative_data, anonymize_snippets=True
    )
    assert entities == {}
    assert total_count == 0
    assert anonymized_text == negative_data
