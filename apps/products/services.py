from uuid import uuid4 as uuid
import django_filters
from apps.products.models import Product
from apps.utils.exceptions import (
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

    def get_all_products(self, filters: dict = {}):
        """Get all products from database"""
        products = self.product_repository.get_all_products(
            fields=["id", "name", "price", "seller_id"]
        )

        return self.ProductFilterSet(filters, products).qs

    def get_product_by_id(self, product_id: uuid):
        """Get a product by its ID"""
        product = self.product_repository.get(pk=product_id)

        if not product:
            raise ResourceNotFoundException(resource_name="Product")

        return product

    def get_product_detail(self, product_id: uuid):
        """Get a product detail by its ID"""
        product = self.product_repository.get_product_detail(
            product_id, fields=["id", "name", "description", "price", "seller_id"]
        )

        if not product:
            raise ResourceNotFoundException(resource_name="Product")

        return product

    def update_product(self, product: Product, **data):
        """Update a product by its ID"""
        return self.product_repository.update(instance=product, **data)

    def delete_product(self, product: Product):
        """Delete a product by its ID"""
        return self.product_repository.delete(instance=product)
