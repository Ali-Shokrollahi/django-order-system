from decimal import Decimal
import pytest


@pytest.fixture
def order_service():
    from apps.orders.services import OrderService

    return OrderService()


@pytest.fixture
def create_order_payload(product_factory):
    product = product_factory.create(price=Decimal("99.99"))
    return {"products_data": [{"product_id": str(product.id), "quantity": 2}]}
