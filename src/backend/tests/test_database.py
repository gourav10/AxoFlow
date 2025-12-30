"""Tests for database module."""

import pytest
import base64
from unittest.mock import MagicMock, patch, Mock
import requests
from app.database import (
    NocoDBClient,
    db,
    create_candidate,
    get_candidate_by_email,
    get_candidate_by_id,
    update_candidate
)


class TestNocoDBClient:
    """Tests for NocoDBClient class."""

    def test_init(self):
        """Test NocoDBClient initialization."""
        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "test-token"
            mock_settings.NOCODB_BASE_ID = "base123"
            mock_settings.NOCODB_TABLE_ID = "table456"

            client = NocoDBClient()

            assert client.base_url == "https://test.com"
            assert client.api_token == "test-token"
            assert client.base_id == "base123"
            assert client.table_id == "table456"
            assert client.api_endpoint == "https://test.com/api/v1/db/data/v1/base123/table456"
            assert client.headers["xc-token"] == "test-token"
            assert client.headers["Content-Type"] == "application/json"

    @patch('app.database.requests.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": "test"}
        mock_request.return_value = mock_response

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client._make_request("GET", "/test")

            assert result == {"success": True, "data": "test"}
            mock_request.assert_called_once()

    @patch('app.database.requests.request')
    def test_make_request_failure(self, mock_request):
        """Test failed API request."""
        mock_request.side_effect = requests.exceptions.RequestException("Connection error")

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()

            with pytest.raises(Exception, match="NocoDB API error"):
                client._make_request("GET", "/test")

    @patch.object(NocoDBClient, '_make_request')
    def test_create_record(self, mock_make_request):
        """Test creating a record."""
        mock_make_request.return_value = {"Id": 1, "email": "test@example.com"}

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            data = {"email": "test@example.com", "name": "Test"}
            result = client.create_record(data)

            assert result["Id"] == 1
            mock_make_request.assert_called_once_with("POST", "", json=data)

    @patch.object(NocoDBClient, '_make_request')
    def test_get_record_success(self, mock_make_request):
        """Test getting a record successfully."""
        mock_make_request.return_value = {"Id": 123, "email": "user@example.com"}

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.get_record(123)

            assert result["Id"] == 123
            mock_make_request.assert_called_once_with("GET", "/123")

    @patch.object(NocoDBClient, '_make_request')
    def test_get_record_not_found(self, mock_make_request):
        """Test getting a non-existent record."""
        mock_make_request.side_effect = Exception("Not found")

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.get_record(999)

            assert result is None

    @patch.object(NocoDBClient, '_make_request')
    def test_list_records(self, mock_make_request):
        """Test listing records."""
        mock_make_request.return_value = {
            "list": [
                {"Id": 1, "email": "user1@example.com"},
                {"Id": 2, "email": "user2@example.com"}
            ]
        }

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.list_records()

            assert len(result) == 2
            assert result[0]["Id"] == 1

    @patch.object(NocoDBClient, '_make_request')
    def test_list_records_with_filter(self, mock_make_request):
        """Test listing records with filter."""
        mock_make_request.return_value = {"list": [{"Id": 1}]}

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.list_records(where="(email,eq,test@example.com)", limit=10, offset=5)

            mock_make_request.assert_called_once()
            call_args = mock_make_request.call_args
            assert call_args[1]["params"]["where"] == "(email,eq,test@example.com)"
            assert call_args[1]["params"]["limit"] == 10
            assert call_args[1]["params"]["offset"] == 5

    @patch.object(NocoDBClient, '_make_request')
    def test_update_record(self, mock_make_request):
        """Test updating a record."""
        mock_make_request.return_value = {"Id": 1, "email": "updated@example.com"}

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            data = {"email": "updated@example.com"}
            result = client.update_record(1, data)

            assert result["email"] == "updated@example.com"
            mock_make_request.assert_called_once_with("PATCH", "/1", json=data)

    @patch.object(NocoDBClient, '_make_request')
    def test_delete_record_success(self, mock_make_request):
        """Test deleting a record successfully."""
        mock_make_request.return_value = {}

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.delete_record(1)

            assert result is True
            mock_make_request.assert_called_once_with("DELETE", "/1")

    @patch.object(NocoDBClient, '_make_request')
    def test_delete_record_failure(self, mock_make_request):
        """Test deleting a record with failure."""
        mock_make_request.side_effect = Exception("Delete failed")

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.delete_record(1)

            assert result is False

    @patch.object(NocoDBClient, 'list_records')
    def test_find_by_email_found(self, mock_list_records):
        """Test finding candidate by email when found."""
        mock_list_records.return_value = [{"Id": 1, "email": "test@example.com"}]

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.find_by_email("test@example.com")

            assert result is not None
            assert result["email"] == "test@example.com"
            mock_list_records.assert_called_once_with(where="(email,eq,test@example.com)", limit=1)

    @patch.object(NocoDBClient, 'list_records')
    def test_find_by_email_not_found(self, mock_list_records):
        """Test finding candidate by email when not found."""
        mock_list_records.return_value = []

        with patch('app.database.settings') as mock_settings:
            mock_settings.NOCODB_URL = "https://test.com"
            mock_settings.NOCODB_API_TOKEN = "token"
            mock_settings.NOCODB_BASE_ID = "base"
            mock_settings.NOCODB_TABLE_ID = "table"

            client = NocoDBClient()
            result = client.find_by_email("notfound@example.com")

            assert result is None


class TestHelperFunctions:
    """Tests for helper functions."""

    @patch.object(NocoDBClient, 'create_record')
    def test_create_candidate(self, mock_create_record):
        """Test create_candidate helper function."""
        mock_create_record.return_value = {
            "Id": 1,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }

        result = create_candidate("test@example.com", "John", "Doe", "password123")

        assert result["Id"] == 1
        assert result["email"] == "test@example.com"

        # Verify the password was base64 encoded
        call_args = mock_create_record.call_args[0][0]
        encoded_password = call_args["password"]
        decoded = base64.b64decode(encoded_password.encode()).decode()
        assert decoded == "password123"

    @patch.object(NocoDBClient, 'find_by_email')
    def test_get_candidate_by_email(self, mock_find_by_email):
        """Test get_candidate_by_email helper function."""
        mock_find_by_email.return_value = {"Id": 1, "email": "test@example.com"}

        result = get_candidate_by_email("test@example.com")

        assert result["email"] == "test@example.com"
        mock_find_by_email.assert_called_once_with("test@example.com")

    @patch.object(NocoDBClient, 'get_record')
    def test_get_candidate_by_id(self, mock_get_record):
        """Test get_candidate_by_id helper function."""
        mock_get_record.return_value = {"Id": 123, "email": "test@example.com"}

        result = get_candidate_by_id(123)

        assert result["Id"] == 123
        mock_get_record.assert_called_once_with(123)

    @patch.object(NocoDBClient, 'update_record')
    def test_update_candidate(self, mock_update_record):
        """Test update_candidate helper function."""
        mock_update_record.return_value = {
            "Id": 1,
            "email": "updated@example.com"
        }

        data = {"email": "updated@example.com"}
        result = update_candidate(1, data)

        assert result["email"] == "updated@example.com"
        mock_update_record.assert_called_once_with(1, data)

    def test_global_db_instance(self):
        """Test that global db instance exists."""
        assert db is not None
        assert isinstance(db, NocoDBClient)
