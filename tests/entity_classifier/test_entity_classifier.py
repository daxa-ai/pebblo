import pytest

from pebblo.entity_classifier.entity_classifier import EntityClassifier
from tests.entity_classifier.mock_response import (
    mock_input_text1_anonymize_snippet_true,
    mock_input_text2_anonymize_snippet_true,
)
from tests.entity_classifier.test_data import (
    input_text1,
    input_text2,
    negative_data,
    tf_test_data,
)


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
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "github-token": 1,
        "slack-token": 2,
        "ip-address": 1,
        "azure-client-secret": 1,
    }
    assert total_count == 13
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
        "aws-access-key": [
            {
                "location": "1472_1492",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "aws-secret-key": [
            {
                "location": "1513_1554",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "1571_1661",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "slack-token": [
            {
                "location": "1735_1758",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1773_1830",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "ip-address": [
            {
                "location": "1904_1915",
                "confidence_score": "HIGH",
                "entity_group": "pii-network",
            }
        ],
        "azure-client-secret": [
            {
                "location": "1939_1975",
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
        "aws-access-key": 1,
        "aws-secret-key": 1,
        "github-token": 1,
        "slack-token": 2,
        "ip-address": 1,
        "azure-client-secret": 1,
    }
    assert total_count == 13
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
        "aws-access-key": [
            {
                "location": "1494_1516",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "aws-secret-key": [
            {
                "location": "1537_1559",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "github-token": [
            {
                "location": "1576_1596",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ],
        "slack-token": [
            {
                "location": "1670_1689",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
            {
                "location": "1704_1723",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            },
        ],
        "ip-address": [
            {
                "location": "1797_1815",
                "confidence_score": "HIGH",
                "entity_group": "pii-network",
            }
        ],
        "azure-client-secret": [
            {
                "location": "1839_1866",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
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


def test_entity_classifier_and_anonymizer_azure_secret(entity_classifier):
    """
    UT for presidio_entity_classifier_and_anonymizer function with tf_test_data
    """
    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(tf_test_data)
    assert entities == {
        "azure-client-secret": 1,
    }
    assert total_count == 1
    assert anonymized_text == tf_test_data
    assert entity_details == {
        "azure-client-secret": [
            {
                "location": "430_466",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ]
    }

    (
        entities,
        total_count,
        anonymized_text,
        entity_details,
    ) = entity_classifier.presidio_entity_classifier_and_anonymizer(tf_test_data, True)
    assert entities == {
        "azure-client-secret": 1,
    }
    assert total_count == 1
    assert entity_details == {
        "azure-client-secret": [
            {
                "location": "430_457",
                "confidence_score": "HIGH",
                "entity_group": "secrets_and_tokens",
            }
        ]
    }
