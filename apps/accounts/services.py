from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import TokenError
from mail_templated import EmailMessage

from apps.utils.exceptions import (
    BadRequestException,
    ResourceAlreadyExistsException,
    ExternalServiceException,
    ResourceNotFoundException,
)
from .repositories import UserRepository


class EmailVerificationToken(Token):
    lifetime = timedelta(hours=1)
    token_type = "email_verification"


class UserService:
    user_repository = UserRepository()

    def create_user(self, *, email: str, password: str):
        """Create a new user in database"""

        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ResourceAlreadyExistsException(
                resource_name="User", identifier="email"
            )

        return self.user_repository.create_user(email, password)

    def register_user(self, *, email: str, password: str):
        """Proccess user registration"""

        user = self.create_user(email=email, password=password)
        self.send_verification_email(user=user)
        return user


    def send_verification_email(self, *, user) -> None:
        token = EmailVerificationToken.for_user(user)
        verification_url = (
            f"{settings.APP_DOMAIN}{reverse('email_verify', args=[token])}"
        )

        message = EmailMessage(
            "email_verification.html",
            {"user": user, "activation_url": verification_url},
            from_email=settings.FROM_EMAIL,
            to=[user.email],
        )
        try:
            message.send()
        except Exception as e:
            raise ExternalServiceException(
                service_name="Email service", extra={"service message": str(e)}
            )

    def verify_user_email(self, *, token):
        try:
            email_token = EmailVerificationToken(token=token)
        except TokenError as e:
            raise BadRequestException(message=str(e))
        user_id = email_token.payload.get("user_id")
        if not user_id:
            raise BadRequestException(message="Invalid token payload")
        user = self.user_repository.get_by_id(id=user_id)
        if user.is_verified:
            raise BadRequestException(message="This account is already verified")
        return self.user_repository.update_user_verification(user=user)

    def resend_verification_email(self, *, email: str) -> None:
        """Resend verification email to an unverified user"""
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ResourceNotFoundException(resource_name="User")
        if user.is_verified:
            raise BadRequestException(message="This account is already verified")
        self.send_verification_email(user=user)
