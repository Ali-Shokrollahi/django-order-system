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

    def get_all_products(self) -> QuerySet[Product]:
        return self.model.objects.only("id", "name", "price", "seller_id").all()

    def get_product_detail(self, product_id: uuid) -> Product:
        return (
            Product.objects.select_related("seller")
            .only("id", "name", "price", "description", "seller__id", "seller__email")
            .filter(id=product_id)
            .first()
        )

