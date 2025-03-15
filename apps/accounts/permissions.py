from rest_framework.permissions import BasePermission
from apps.accounts.models import User


class IsSellerPermission(BasePermission):
    """Permission to allow only users with the 'seller' role."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role == User.RoleChoices.SELLER
        )


class IsOwnerPermission(BasePermission):
    """
    Permission to allow only the owner of the resource.
    """

    def has_object_permission(self, request, view, obj):
        try:
            owner = getattr(obj, view.owner_field, "seller")
            return owner == request.user
        except AttributeError:
            # Return False if the specified field doesn't exist
            return False
