import pytest
from rest_framework.test import APIClient
from .factories import UserFactory


@pytest.fixture
def api_client():
    """Fixture to provide API client."""
    return APIClient()


@pytest.fixture
def seller():
    return UserFactory.create(role="seller", is_active=True, is_verified=True)


@pytest.fixture
def customer():
    return UserFactory.create(is_active=True, is_verified=True)


@pytest.fixture
def api_request(api_client):
    def _request(method, url, payload=None, user=None, query_params=None):
        if user:
            api_client.force_authenticate(user=user)

        match method:
            case "get":
                return api_client.get(url, data=query_params)
            case "post":
                return api_client.post(url, payload, format="json")
            case "put":
                return api_client.put(url, payload, format="json")
            case "patch":
                return api_client.patch(url, payload, format="json")
            case "delete":
                return api_client.delete(url)
            case _:
                raise ValueError(f"Unsupported HTTP method: {method}")

    return _request
