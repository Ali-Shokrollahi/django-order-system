import pytest
from django.core import mail

from apps.accounts.services import UserService
from tests.factories import UserFactory


@pytest.fixture
def user_service():
    """Fixture for UserService instance."""
    return UserService()


@pytest.fixture
def unverified_user():
    """Fixture for an unverified user."""
    return UserFactory.create()


@pytest.fixture
def verified_user():
    """Fixture for a verified user."""
    return UserFactory.create(is_verified=True, is_active=True)


@pytest.fixture(autouse=True)
def clear_mail_outbox():
    """Fixture to clear mail.outbox before each test."""
    mail.outbox.clear()


@pytest.fixture
def create_user_data():
    """Fixture for a valid user creation"""
    return {
        "email": "user@example.com",
        "password": "securepassword123",
    }
