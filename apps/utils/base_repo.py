from typing import TypeVar, Generic
from django.db.models import Model, QuerySet

T = TypeVar("T", bound=Model)

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def get(self, **filters) -> T | None:
        """Get a single object or return None if not found."""
        return self.model.objects.filter(**filters).first()

    def filter(self, **filters) -> QuerySet[T]:
        """Get a queryset of filtered objects."""
        return self.model.objects.filter(**filters)

    def create(self, **data) -> T:
        """Create a new object."""
        return self.model.objects.create(**data)

    def update(self, instance: T, **data) -> T:
        """Update an instance."""
        self.model.objects.filter(pk=instance.pk).update(**data)
        instance.refresh_from_db()
        return instance

    def delete(self, instance: T) -> None:
        """Delete an instance."""
        instance.delete()
