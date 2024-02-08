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


# DocHelper
@pytest.fixture(scope="module")
def doc_helper():
    with patch('pebblo.app.service.service.DocHelper') as doc_helper:
        yield doc_helper


# Reports
@pytest.fixture(scope="module")
def reports():
    with patch('pebblo.app.service.service.Reports') as reports:
        yield reports


@pytest.fixture
def mock_read_json_file():
    with patch('pebblo.app.service.service.read_json_file') as mock_read_json_file:
        yield mock_read_json_file


@pytest.fixture
def mock_write_json_to_file():
    with patch('pebblo.app.service.service.write_json_to_file') as mock_write_json_to_file:
        yield mock_write_json_to_file


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


def test_loader_doc_success(mock_write_json_to_file, mock_read_json_file, doc_helper, reports):
    """
    Test the loader doc endpoint success.
    """
    mock_write_json_to_file.return_value = None
    mock_read_json_file.return_value = {"app": "Test App"}

    doc_helper_instance = doc_helper.return_value
    doc_helper_instance.process_docs_and_generate_report = Mock()
    doc_helper_instance.process_docs_and_generate_report.return_value = ({"details": 1}, {"final_report": 1})

    reports_instance = reports.return_value
    reports_instance.generate_report = Mock()
    reports_instance.generate_report.return_value = None

    loader_doc = {
        'name': 'Test App',
        'owner': 'User',
        'source_owner': 'User',
        'load_id': '41fdd94e-f68b-4af1-b5d5-7243d2bb2ff6',
        'loading_end': True,
        'docs': [
            {
                'doc': 'Sample content',
                'source_path': '/fake/path/topic_data.csv',
                'last_modified': None,
                'file_owner': 'User',
                'source_path_size': 307
            }
        ],
        'loader_details': {
            'loader': 'CSVLoader',
            'source_path': '/fake/path/topic_data.csv',
            'source_type': 'file',
            'source_path_size': 307,
            'source_aggr_size': 306
        },
        'plugin_version': '0.1.0'
    }
    response = client.post("/v1/loader/doc", json=loader_doc)
    assert response.status_code == 200
    assert response.json() == {"message": "Loader Doc API Request processed successfully"}
