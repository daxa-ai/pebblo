import json
from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from pebblo.app import daemon
from pebblo.app.routers.routers import router_instance

app = FastAPI()
app.include_router(router_instance.router)

client = TestClient(app)


app_discover_payload = {
    "name": "Test App",
    "owner": "Test owner",
    "description": "This is a test app.",
    "runtime": {
        "type": "desktop",
        "host": "MacBook-Pro.local",
        "path": "Test/Path",
        "ip": "127.0.0.1",
        "platform": "macOS-14.6.1-arm64-i386-64bit",
        "os": "Darwin",
        "os_version": "Darwin Kernel Version 23.6.0",
        "language": "python",
        "language_version": "3.11.9",
        "runtime": "Mac OSX",
    },
    "framework": {"name": "langchain", "version": "0.2.35"},
    "plugin_version": "0.1",
    "client_version": {"name": "langchain_community", "version": "0.2.12"},
}


@pytest.fixture(scope="module")
def mocked_objects():
    with (
        patch.object(daemon, "start", "TopicClassifier") as topic_classifier,
        patch.object(daemon, "start", "EntityClassifier") as entity_classifier,
    ):
        yield topic_classifier, entity_classifier


@pytest.fixture(scope="module")
def topic_classifier():
    with patch.object(daemon, "start", "TopicClassifier") as topic_classifier:
        yield topic_classifier


@pytest.fixture(scope="module")
def entity_classifier():
    with patch.object(daemon, "start", "EntityClassifier") as entity_classifier:
        yield entity_classifier


# DocHelper
@pytest.fixture(scope="module")
def doc_helper():
    with patch("pebblo.app.service.service.LoaderHelper") as doc_helper:
        yield doc_helper


# Reports
@pytest.fixture(scope="module")
def reports():
    with patch("pebblo.app.service.service.Reports") as reports:
        yield reports


@pytest.fixture
def mock_read_json_file():
    with patch("pebblo.app.service.service.read_json_file") as mock_read_json_file:
        yield mock_read_json_file


@pytest.fixture
def mock_write_json_to_file():
    with patch(
        "pebblo.app.service.discovery_service.AppDiscover._write_file_content_to_path"
    ) as mock_write_json_to_file:
        yield mock_write_json_to_file


@pytest.fixture
def mock_pebblo_server_version():
    # Mocking the get_pebblo_server_version function
    with patch(
        "pebblo.app.service.discovery_service.get_pebblo_server_version"
    ) as mock_get_pebblo_server_version:
        # Set the return value of the mocked function
        mock_get_pebblo_server_version.return_value = "x.x.x"
        yield mock_get_pebblo_server_version


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


def test_app_discover_success(mock_write_json_to_file, mock_pebblo_server_version):
    """
    Test the app discover endpoint.
    """
    mock_write_json_to_file.return_value = None
    response = client.post("/v1/app/discover", json=app_discover_payload)

    # Assertions
    assert response.status_code == 200
    assert response.json()["pebblo_server_version"] == "x.x.x"
    assert response.json()["message"] == "App Discover Request Processed Successfully"


def test_app_discover_validation_errors(mock_write_json_to_file):
    """
    Test the app discover endpoint with validation errors.
    """
    mock_write_json_to_file.return_value = None
    app_payload = app_discover_payload.copy()
    app_payload.pop("name")

    response = client.post("/v1/app/discover", json=app_payload)
    assert response.status_code == 422
    assert "'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required'" in str(
        response.json()["detail"]
    )


def test_app_discover_server_error(mock_write_json_to_file):
    """
    Test the app discover endpoint with server error.
    """
    mock_write_json_to_file.side_effect = Exception("Mocked exception")
    response = client.post("/v1/app/discover", json=app_discover_payload)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"message": "Mocked exception"}


def test_loader_doc_success(
    mock_write_json_to_file, mock_read_json_file, doc_helper, reports
):
    """
    Test the loader doc endpoint success.
    """
    mock_write_json_to_file.return_value = None
    mock_read_json_file.return_value = {"app": "Test App"}

    doc_helper_instance = doc_helper.return_value
    doc_helper_instance.process_docs_and_generate_report = Mock()
    doc_helper_instance.process_docs_and_generate_report.return_value = (
        {"details": 1},
        {"final_report": 1},
    )

    reports_instance = reports.return_value
    reports_instance.generate_report = Mock()
    reports_instance.generate_report.return_value = None, None

    loader_doc = {
        "name": "Test App",
        "owner": "User",
        "source_owner": "User",
        "load_id": "41fdd94e-f68b-4af1-b5d5-7243d2bb2ff6",
        "loading_end": True,
        "docs": [
            {
                "doc": "Sample content",
                "source_path": "/fake/path/topic_data.csv",
                "last_modified": None,
                "file_owner": "User",
                "source_path_size": 307,
            }
        ],
        "loader_details": {
            "loader": "CSVLoader",
            "source_path": "/fake/path/topic_data.csv",
            "source_type": "file",
            "source_path_size": 307,
            "source_aggr_size": 306,
        },
        "plugin_version": "0.1.0",
        "classifier_location": "local",
    }
    response = client.post("/v1/loader/doc", json=loader_doc)
    assert response.status_code == 200
    assert json.loads(response.text) == {
        "docs": [],
        "message": "Loader Doc API Request processed successfully",
    }
