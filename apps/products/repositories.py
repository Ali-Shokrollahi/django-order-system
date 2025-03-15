from uuid import uuid4 as uuid
from django.db.models import QuerySet
from apps.utils.base_repo import BaseRepository
from .models import Product


class ProductRepository(BaseRepository[Product]):
    """Handles database operations for the Product model."""

    def __init__(self):
        super().__init__(Product)

    def create_product(
        self, *, name: str, description: str | None, price: float, seller
    ) -> Product:
        return self.create(
            name=name, description=description, price=price, seller=seller
        )

    def get_all_products(self, fields: list[str]) -> QuerySet[Product]:
        return self.model.objects.only(*fields).all()

    def get_products_by_ids(
        self, product_ids: list[uuid], fields: list[str]
    ) -> QuerySet[Product]:
        """Fetch multiple products by their IDs in one query."""
        return self.model.objects.filter(id__in=product_ids).only(*fields)

    def get_product_detail(self, product_id: uuid, fields: list[str]) -> Product:
        return (
            Product.objects.select_related("seller")
            .only(*fields)
            .filter(id=product_id)
            .first()
        )
