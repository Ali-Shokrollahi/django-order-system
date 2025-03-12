from rest_framework.permissions import BasePermission
from apps.accounts.models import User


class IsSellerPermission(BasePermission):
    """Permission to allow only users with the 'seller' role."""
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "role") and
            request.user.role == User.RoleChoices.SELLER
        )