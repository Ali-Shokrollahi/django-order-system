from rest_framework.exceptions import ValidationError
from .repositories import UserRepository

class UserService:
    user_repository = UserRepository()

    def create_user(self, *, email: str, password: str):
        """Create a new user in database"""
        
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValidationError("User with this email already exists.", code="user_already_exist")
        return UserRepository.create_user(email, password)
    
    def register_user(self, *, email: str, password: str):
        """Proccess user registration"""

        user = self.create_user(email=email, password=password)
        return user

