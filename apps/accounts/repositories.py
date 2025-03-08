from django.contrib.auth import get_user_model

from apps.utils.base_repo import BaseRepository

User = get_user_model()


class UserRepository(BaseRepository[User]):
    """Handles database operations for the User model."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str):
        """Retrieve a user by email."""
        return self.get(email=email)

    def get_by_id(self, id: int):
        """Retrieve a user by id."""
        return self.get(pk=id)

    def create_user(self, email: str, password: str):
        """Creates a new user."""
        user = User.objects.create_user(email=email, password=password)  # type: ignore
        return user

    def update_user_verification(self, user):
        fields = {"is_verified": True, "is_active": True}
        updated_user = self.update(user, **fields)
        return updated_user
