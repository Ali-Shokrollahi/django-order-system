import pytest
from tests.factories import ProductFactory


@pytest.fixture
def product_service():
    from apps.products.services import ProductService

    return ProductService()


@pytest.fixture
def product_factory():
    return ProductFactory


@pytest.fixture
def product(seller):
    return ProductFactory.create(seller=seller)


@pytest.fixture
def create_product_payload():
    return {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": "999.99",
    }


@pytest.fixture
def update_product_payload():
    return {"name": "Updated Laptop", "price": "1499.99"}
