import django_filters
from apps.products.models import Product
from apps.utils.exceptions import (
    BadRequestException,
    ResourceAlreadyExistsException,
    ExternalServiceException,
    ResourceNotFoundException,
)
from .repositories import ProductRepository


class ProductService:
    product_repository = ProductRepository()

    class ProductFilterSet(django_filters.FilterSet):
        search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
        price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
        price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
        seller = django_filters.NumberFilter(field_name="seller")

        class Meta:
            model = Product
            fields = ["search", "price_min", "price_max", "seller"]

    def create_product(self, name: str, description: str, price: float, seller):
        """Create a new product in database"""

        return self.product_repository.create_product(
            name=name, description=description, price=price, seller=seller
        )

    def get_all_products(self, filters: dict = dict()):
        """Get all products from database"""
        products = self.product_repository.get_all_products()

        return self.ProductFilterSet(filters, products).qs
