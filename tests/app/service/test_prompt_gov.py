# test_prompt_gov.py
from unittest.mock import patch

import pytest

from pebblo.app.service.prompt_gov import PromptGov


@pytest.fixture
def mock_entity_classifier():
    with patch("pebblo.app.service.prompt_gov.EntityClassifier") as mock:
        yield mock


def test_process_request_success(mock_entity_classifier):
    mock_entity_classifier_instance = mock_entity_classifier.return_value
    mock_entity_classifier_instance.presidio_entity_classifier_and_anonymizer.return_value = (
        {"us-ssn": 1},
        1,
        "anonymized document",
    )

    data = {"prompt": "Sachin's SSN is 222-85-4836"}
    prompt_gov = PromptGov(data)
    response = prompt_gov.process_request()

    expected_response = {
        "message": "Prompt Gov Processed Successfully",
        "entities": {"us-ssn": 1},
    }

    assert response == expected_response


if __name__ == "__main__":
    pytest.main()
