from uuid import uuid4 as uuid
from django.db.models import QuerySet
import django_filters
from apps.utils.base_repo import BaseRepository
from .models import Product


class ProductRepository(BaseRepository[Product]):
    """Handles database operations for the Product model."""

    def __init__(self):
        super().__init__(Product)

    class FilterSet(django_filters.FilterSet):
        search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
        price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
        price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
        seller = django_filters.NumberFilter(field_name="seller")

        class Meta:
            model = Product
            fields = ["search", "price_min", "price_max", "seller"]

    def create_product(
        self, *, name: str, description: str | None, price: float, seller
    ) -> Product:
        return self.create(
            name=name, description=description, price=price, seller=seller
        )

    def get_all_products(
        self, filters: dict = {}, fields: list[str] = []
    ) -> QuerySet[Product]:
        return self.FilterSet(filters, self.all().only(*fields)).qs

    def get_products_by_ids(
        self, product_ids: list[uuid], fields: list[str] = []
    ) -> QuerySet[Product]:
        """Fetch multiple products by their IDs in one query."""
        return self.filter(id__in=product_ids).only(*fields)

    def get_product_and_seller_by_id(
        self, product_id: uuid, fields: list[str] = []
    ) -> Product:
        return self.filter(id=product_id).select_related("seller").only(*fields).first()

    def get_products_by_seller(self, seller_id: int) -> QuerySet[Product]:
        return self.filter(seller_id=seller_id)
