from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from apps.utils.models import TimeStampModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.role = self.model.RoleChoices.ADMIN
        user.save(using=self._db)

        return user


class User(TimeStampModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username.
    """

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer"
        SELLER = "seller"
        ADMIN = "admin"

    email = models.EmailField(verbose_name="email address", unique=True)

    role = models.CharField(
        max_length=10, choices=RoleChoices, default=RoleChoices.CUSTOMER
    )

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.role == self.RoleChoices.ADMIN
