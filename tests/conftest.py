import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Fixture to provide API client."""
    return APIClient()

@pytest.fixture
def api_post_request(api_client):
    """Helper fixture to make POST requests."""
    def _post(url, payload):
        return api_client.post(url, payload, format="json")
    return _post


@pytest.fixture
def api_get_request(api_client):
    """Helper fixture to make GET requests."""
    def _get(url):
        return api_client.get(url)
    return _get