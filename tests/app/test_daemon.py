from unittest.mock import Mock
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from pebblo.app.routers.routers import router_instance

app = FastAPI()
app.include_router(router_instance.router)

client = TestClient(app)


@pytest.fixture(scope="module")
def mocked_objects():
    with patch('pebblo.app.daemon.TopicClassifier') as topic_classifier, \
            patch('pebblo.app.daemon.EntityClassifier') as entity_classifier:
        yield topic_classifier, entity_classifier


@pytest.fixture(scope="module")
def topic_classifier():
    with patch('pebblo.app.daemon.TopicClassifier') as topic_classifier:
        yield topic_classifier


@pytest.fixture(scope="module")
def entity_classifier():
    with patch('pebblo.app.daemon.EntityClassifier') as entity_classifier:
        yield entity_classifier


def test_topic_classifier(topic_classifier):
    assert topic_classifier is not None


def test_entity_classifier(entity_classifier):
    assert entity_classifier is not None


def test_root_endpoint():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@patch('pebblo.app.service.service.write_json_to_file', return_value=Mock())
def test_app_discover_success(mock_write_json_to_file):
    """
    Test the app discover endpoint.
    """
    mock_write_json_to_file.return_value = None
    app_payload = {
        "name": "Test App",
        "owner": "Test owner",
        "description": "This is a test app.",
        "plugin_version": "0.1"
    }
    response = client.post("/v1/app/discover", json=app_payload)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "App Discover Request Processed Successfully"}


@patch('pebblo.app.service.service.write_json_to_file', return_value=Mock())
def test_app_discover_validation_errors(mock_write_json_to_file):
    """
    Test the app discover endpoint with validation errors.
    """
    mock_write_json_to_file.return_value = None
    app = {
        "owner": "Test owner",
        "description": "This is a test app.",
        "plugin_version": "0.1"
    }
    response = client.post("/v1/app/discover", json=app)
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert "name\n  none is not an allowed value (type=type_error.none.not_allowed)" in detail


@patch('pebblo.app.service.service.write_json_to_file', return_value=Mock())
def test_app_discover_server_error(mock_write_json_to_file):
    """
    Test the app discover endpoint with server error.
    """
    mock_write_json_to_file.side_effect = Exception("Mocked exception")
    app_payload = {
        "name": "Test App",
        "owner": "Test owner",
        "description": "This is a test app.",
        "plugin_version": "0.1"
    }
    response = client.post("/v1/app/discover", json=app_payload)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
