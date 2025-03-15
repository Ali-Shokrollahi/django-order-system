from decimal import Decimal
import pytest
from apps.orders.models import Order


@pytest.mark.django_db
class TestSellerService:
    """Tests for SellerService class."""

    @pytest.fixture(autouse=True)
    def setup(self, seller_service):
        self.service = seller_service

    def test_get_seller_products_success(self, seller, product_factory):
        """Test retrieving products for a seller."""
        products = product_factory.create_batch(3, seller=seller)

        seller_products = self.service.get_seller_products(seller.id)
        assert seller_products.count() == 3
        assert products[1] in seller_products

    def test_get_seller_products_empty(self, seller):
        """Test retrieving products when none exist."""
        seller_products = self.service.get_seller_products(seller.id)
        assert seller_products.count() == 0

    def test_get_seller_orders_no_filters(
        self,
        seller,
        customer,
        product_factory,
        order_factory,
        order_item_factory,
    ):
        """Test retrieving orders without filters."""
        product1 = product_factory.create(price=Decimal("99.99"), seller=seller)
        product2 = product_factory.create(price=Decimal("149.99"), seller=seller)

        order = order_factory.create(customer=customer)
        order_item1 = order_item_factory.create(
            order=order, product=product1, quantity=2
        )
        order_item2 = order_item_factory.create(
            order=order, product=product2, quantity=1
        )

        seller_orders = self.service.get_seller_orders(seller.id)
        assert order in seller_orders
        assert order_item1 in order.orderitem_set.all()
        assert order_item2 in order.orderitem_set.all()
        assert seller_orders.count() == 1

    def test_get_seller_orders_with_filters(
        self, seller, product_factory, order_factory, order_item_factory, customer
    ):
        """Test retrieving orders with status filter."""

        product1 = product_factory.create(price=Decimal("99.99"), seller=seller)
        product2 = product_factory.create(price=Decimal("149.99"), seller=seller)

        order_pending = order_factory.create(
            customer=customer,
            status=Order.StatusChoices.PENDING,
        )
        order_item_factory.create(order=order_pending, product=product1, quantity=2)
        order_completed = order_factory.create(
            customer=customer,
            status=Order.StatusChoices.COMPLETED,
        )
        order_item_factory.create(order=order_completed, product=product2, quantity=1)

        filters = {"status": Order.StatusChoices.COMPLETED}
        orders = self.service.get_seller_orders(seller.id, filters)
        assert orders.count() == 1
        assert order_completed in orders
        assert order_pending not in orders

    def test_get_seller_orders_empty(self, seller):
        """Test retrieving orders when none exist."""
        orders = self.service.get_seller_orders(seller.id)
        assert orders.count() == 0
