import pytest
from decimal import Decimal
from uuid import uuid4
from apps.orders.models import OrderItem, Order
from apps.utils.exceptions import ResourceNotFoundException


@pytest.mark.django_db
class TestOrderService:
    """Tests for OrderService class."""

    @pytest.fixture(autouse=True)
    def setup(self, order_service):
        self.service = order_service

    def test_create_order_success(self, seller, customer, product_factory):
        """Test creating an order with valid products."""
        product = product_factory.create(price=Decimal("99.99"), seller=seller)
        products_data = [{"product_id": str(product.id), "quantity": 2}]

        order = self.service.create_order(
            customer=customer, products_data=products_data
        )

        assert str(order.total_amount) == "199.98"  # 2 * 99.99
        assert order.customer == customer
        assert order.status == Order.StatusChoices.PENDING
        assert OrderItem.objects.filter(order=order).count() == 1
        order_item = OrderItem.objects.get(order=order, product=product)
        assert order_item.quantity == 2

    def test_create_order_multiple_products(self, seller, customer, product_factory):
        """Test creating an order with multiple products."""
        product1 = product_factory.create(price=Decimal("99.99"), seller=seller)
        product2 = product_factory.create(price=Decimal("149.99"), seller=seller)
        products_data = [
            {"product_id": str(product1.id), "quantity": 1},
            {"product_id": str(product2.id), "quantity": 2},
        ]

        order = self.service.create_order(
            customer=customer, products_data=products_data
        )

        assert str(order.total_amount) == "399.97"
        assert OrderItem.objects.filter(order=order).count() == 2

        assert OrderItem.objects.get(order=order, product=product1).quantity == 1
        assert OrderItem.objects.get(order=order, product=product2).quantity == 2

    def test_create_order_missing_product(self, customer):
        """Test creating an order with a non-existent product raises an exception."""
        product_id = str(uuid4())
        products_data = [{"product_id": product_id, "quantity": 1}]

        with pytest.raises(ResourceNotFoundException) as exc:
            self.service.create_order(customer=customer, products_data=products_data)
        assert "Product not found" in str(exc.value)
        assert exc.value.extra["missing_products"] == [product_id]
        assert Order.objects.count() == 0
