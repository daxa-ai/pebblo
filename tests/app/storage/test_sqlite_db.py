from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from pebblo.app.models.sqltables import (
    AiDataSourceTable,
    AiSnippetsTable,
)

# Assume table_obj is imported from the actual module where the table is defined


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

    # Call the method
    success, result = sqlite_client.query_by_list(table_obj, filter_key, filter_values)

    # Assertions
    assert success is True
    assert result == ["result1", "result2"]

    # Ensure the query was called only once (no pagination)
    assert mock_session.query().filter().all.call_count == 1


def test_query_by_list_page_size(sqlite_client):
    """Test successful query with query_by_list to verify max_filter_limit"""
    mock_session = sqlite_client.session
    table_obj = AiSnippetsTable
    filter_key = "id"
    filter_values = [
        "snippet_id1",
        "snippet_id2",
        "snippet_id3",
        "snippet_id4",
        "snippet_id5",
    ]
    page_size = 2

    # Mocking query result
    mock_result_page_1 = ["result1", "result2"]
    mock_result_page_2 = ["result3", "result4"]
    mock_result_page_3 = ["result5"]
    mock_query = mock_session.query().filter().all
    mock_query.side_effect = [
        mock_result_page_1,
        mock_result_page_2,
        mock_result_page_3,
    ]

    # Call the method
    success, result = sqlite_client.query_by_list(
        table_obj, filter_key, filter_values, page_size
    )

    # Assertions
    assert success is True
    assert result == ["result1", "result2", "result3", "result4", "result5"]


def test_query_by_list_failure(sqlite_client):
    mock_session = sqlite_client.session
    mock_table_obj = AiSnippetsTable
    filter_key = "id"
    filter_values = ["value1", "value2"]

    # Create mock data
    page_size = "abcd"  # invalid page size

    # Call the query_by_list function
    success, results = sqlite_client.query_by_list(
        table_obj=mock_table_obj,
        filter_key=filter_key,
        filter_values=filter_values,
        page_size=page_size,
    )

    assert success is False
    assert results == []
    mock_session.query.assert_not_called()
