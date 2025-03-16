import pytest
import requests
from unittest.mock import patch
from requests.models import Response
from src.requests_sync import RequestsSync


@pytest.fixture
def mock_requests():
    """Fixture to mock the requests module."""
    with patch("requests.request") as mock:
        yield mock


def test_send_request_success(mock_requests):
    """Test the send_request method for a successful request."""

    # Prepare mock response
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b'{"key": "value"}'  # Simulating a JSON response
    mock_requests.return_value = mock_response

    base_url = "http://example.com"
    client = RequestsSync(base_url)

    # Call the method
    result = client.send_request(endpoint="test-endpoint")

    # Assertions
    mock_requests.assert_called_once_with(
        method="GET", url="http://example.com/test-endpoint", params=None
    )
    assert result == {"key": "value"}  # Check if the result is as expected


def test_send_request_error(mock_requests):
    """Test the send_request method when an exception occurs."""

    # Prepare mock to raise an exception
    mock_requests.side_effect = requests.exceptions.RequestException("Network error")

    base_url = "http://example.com"
    client = RequestsSync(base_url)

    # Call the method
    result = client.send_request(endpoint="test-endpoint")

    # Assertions
    mock_requests.assert_called_once_with(
        method="GET", url="http://example.com/test-endpoint", params=None
    )
    assert result is None  # Check if the result is None after the error


def test_send_request_with_params(mock_requests):
    """Test the send_request method with parameters."""

    # Prepare mock response
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b'{"key": "value"}'
    mock_requests.return_value = mock_response

    base_url = "http://example.com"
    client = RequestsSync(base_url)

    params = {"param1": "value1", "param2": "value2"}
    result = client.send_request(endpoint="test-endpoint", params=params)

    # Assertions
    mock_requests.assert_called_once_with(
        method="GET", url="http://example.com/test-endpoint", params=params
    )
    assert result == {"key": "value"}


def test_send_request_with_post_method(mock_requests):
    """Test the send_request method with POST method."""

    # Prepare mock response
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b'{"key": "value"}'
    mock_requests.return_value = mock_response

    base_url = "http://example.com"
    client = RequestsSync(base_url)

    params = {"param1": "value1"}
    result = client.send_request(endpoint="test-endpoint", method="POST", params=params)

    # Assertions
    mock_requests.assert_called_once_with(
        method="POST", url="http://example.com/test-endpoint", params=params
    )
    assert result == {"key": "value"}
