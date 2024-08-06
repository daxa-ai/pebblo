# test_prompt_gov.py
from unittest.mock import patch

import pytest

import tests.log  # noqa: F401
from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import PromptGovResponseModel
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
        {"us-ssn": [{"location": "16_27", "confidence_score": "HIGH"}]},
    )

    data = {"prompt": "Sachin's SSN is 222-85-4836"}
    prompt_gov = PromptGov(data)
    response = prompt_gov.process_request()
    expected_response = PromptGovResponseModel(
        entities={"us-ssn": 1},
        entityCount=1,
        message="Prompt Governance Processed Successfully",
    )
    expected_response = PebbloJsonResponse.build(
        body=expected_response.dict(exclude_none=True), status_code=200
    )

    assert response.__dict__ == expected_response.__dict__


if __name__ == "__main__":
    pytest.main()
