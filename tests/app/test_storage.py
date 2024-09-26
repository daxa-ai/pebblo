import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql import func
from pebblo.app.models.sqltables import (
    AiSnippetsTable,
)

# Assume table_obj is imported from the actual module where the table is defined


class MockTable(DeclarativeMeta):
    __tablename__ = 'mock_table'
    data = {}


@pytest.fixture
def sqlite_client():
    """Fixture for creating an SQLiteClient instance."""
    from pebblo.app.storage.sqlite_db import SQLiteClient
    client = SQLiteClient()
    client.session = MagicMock(spec=Session)
    return client


def test_query_by_list_success(sqlite_client, mocker):
    """Test successful query with query_by_list."""
    mock_session = sqlite_client.session
    table_obj = AiSnippetsTable
    filter_key = "id"
    filter_values = ["snippet_id1", "snippet_id2"]

    # Mocking query result
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = ["result1", "result2"]  # Mocked results

    # Mock func.json_extract
    mock_json_extract = mocker.patch('sqlalchemy.sql.func.json_extract')

    # Call the method
    success, result = sqlite_client.query_by_list(table_obj, filter_key, filter_values)

    # Ensure that `json_extract` was called with the correct arguments
    mock_json_extract.assert_called_once_with(table_obj.data, f"$.{filter_key}")

    # Assertions
    assert success is True
    assert result == ["result1", "result2"]


def test_query_by_list_failure(sqlite_client, mocker):
    """Test query_by_list failure due to an exception."""
    mock_session = sqlite_client.session
    mock_table_obj = MockTable  # Use your actual table object here
    filter_key = "invalid_key"
    filter_values = ["value1", "value2"]

    # Mocking an exception when calling the query
    mock_session.query.side_effect = Exception("DB Error. Key with name 'invalid_key' does not exists.")

    # Call the method
    success, result = sqlite_client.query_by_list(mock_table_obj, filter_key, filter_values)

    # Assertions
    assert success is False
    assert result == []
    mock_session.query.assert_called_once_with(mock_table_obj)

