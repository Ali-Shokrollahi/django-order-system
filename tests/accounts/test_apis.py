import pytest
from rest_framework import status
from django.urls import reverse

from apps.accounts.services import EmailVerificationToken


@pytest.mark.django_db
class TestUserCreateApi:
    """Tests for UserCreateApi API."""

    @pytest.fixture(autouse=True)
    def setup(self, api_post_request):
        self.post_request = api_post_request
        self.url = reverse("register_user")

    def test_create_user_success(self, create_user_data):
        """Test successful user registration returns correct HTTP response."""
        create_user_data["confirm_password"] = create_user_data["password"]
        response = self.post_request(self.url, create_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == create_user_data["email"]
        assert "created_at" in data

    def test_create_user_password_mismatch(self, create_user_data):
        """Test password mismatch returns 400 with validation error."""
        create_user_data["confirm_password"] = "differentpassword"
        response = self.post_request(self.url, create_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserEmailVerifyApi:
    """Tests for UserEmailVerifyApi API."""

    @pytest.fixture(autouse=True)
    def setup(self, api_get_request):
        self.get_request = api_get_request

    def test_verify_email_success(self, unverified_user):
        """Test successful email verification returns 200."""
        email_verification_token = EmailVerificationToken.for_user(unverified_user)
        url = reverse("email_verify", args=[str(email_verification_token)])

        response = self.get_request(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Email confirmed successfully"


@pytest.mark.django_db
class TestUserResendVerificationApi:
    """Tests for UserResendVerificationApi API."""

    @pytest.fixture(autouse=True)
    def setup(self, api_post_request):
        self.post_request = api_post_request
        self.url = reverse("email_resend")

    def test_resend_verification_success(self, unverified_user):
        """Test successful resend returns 200."""
        payload = {"email": unverified_user.email}
        response = self.post_request(self.url, payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Verification email resent successfully"
        assert response.json()["data"] is None
