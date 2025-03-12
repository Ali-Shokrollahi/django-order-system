import pytest
from django.contrib.auth.hashers import check_password
from django.core import mail
from apps.accounts.services import EmailVerificationToken
from apps.utils.exceptions import (
    ResourceAlreadyExistsException,
    BadRequestException,
    ResourceNotFoundException,
)


@pytest.mark.django_db
class TestUserService:
    """Tests for UserService class."""

    @pytest.fixture(autouse=True)
    def setup(self, user_service):
        self.service = user_service

    def test_create_user_success(self, create_user_data):
        """Test creating a new user successfully."""
        email = create_user_data["email"]
        password = create_user_data["password"]

        user = self.service.create_user(email=email, password=password)

        assert user.email == email
        assert check_password(password, user.password)
        assert user.role == "customer"
        assert not user.is_active
        assert not user.is_verified
        assert not user.is_staff

    def test_create_user_duplicate_email(self, unverified_user):
        """Test creating a user with an existing email raises an exception."""

        with pytest.raises(ResourceAlreadyExistsException) as exc:
            self.service.create_user(
                email=unverified_user.email, password="securepassword123"
            )

        assert "User with this email already exists" in str(exc.value)

    def test_register_user_success(self, create_user_data):
        """Test registering a user sends verification email."""
        email = create_user_data["email"]
        password = create_user_data["password"]

        user = self.service.register_user(email=email, password=password)

        assert user.email == email

    def test_send_verification_email_success(self, unverified_user):
        """Test sending a verification email successfully."""

        self.service.send_verification_email(user=unverified_user)

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]
        assert unverified_user.email in mail.outbox[0].body

    def test_verify_user_email_success(self, unverified_user):
        """Test verifying an email activates the user."""

        email_verification_token = EmailVerificationToken.for_user(unverified_user)

        verified_user = self.service.verify_user_email(
            token=str(email_verification_token)
        )

        assert verified_user.is_verified

    def test_verify_user_email_invalid_token(self):
        """Test verifying with an invalid token raises an exception."""
        with pytest.raises(BadRequestException) as exc:
            self.service.verify_user_email(token="invalid-token")
        assert "invalid" in str(exc.value)

    def test_verify_user_email_already_verified(self, verified_user):
        """Test verifying an already verified user raises an exception."""
        email_verification_token = EmailVerificationToken.for_user(verified_user)

        with pytest.raises(BadRequestException) as exc:
            self.service.verify_user_email(token=str(email_verification_token))
        assert "already verified" in str(exc.value)

    def test_resend_verification_email_success(self, unverified_user):
        """Test resending verification email to an unverified user."""
        self.service.resend_verification_email(email=unverified_user.email)

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [unverified_user.email]

    def test_resend_verification_email_user_not_found(self):
        """Test resending email for a non-existent user raises an exception."""
        # Act & Assert
        with pytest.raises(ResourceNotFoundException) as exc:
            self.service.resend_verification_email(email="nonexistent@example.com")
        assert "User not found" in str(exc.value)

    def test_resend_verification_email_already_verified(self, verified_user):
        """Test resending email for a verified user raises an exception."""
        # Act & Assert
        with pytest.raises(BadRequestException) as exc:
            self.service.resend_verification_email(email=verified_user.email)
        assert "already verified" in str(exc.value)
