from django.db.models import QuerySet, Sum, F
from django.contrib.auth.models import User
from django_filters import FilterSet

from apps.utils.base_repo import BaseRepository
from apps.orders.models import Order, OrderItem


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    class FilterSet(FilterSet):
        class Meta:
            model = Order
            fields = ["status"]

    def create_order(
        self, customer: User, products_data: dict[str, int], total_amount: float
    ) -> Order:
        """
        Create an order with associated order items.
        products_data: List of dicts with 'product' (Product object) and 'quantity'.
        """
        order = self.create(
            customer=customer,
            total_amount=total_amount,
            status=Order.StatusChoices.PENDING,
        )

        order_items = [
            OrderItem(order=order, product_id=product, quantity=quantity)
            for product, quantity in products_data.items()
        ]
        OrderItem.objects.bulk_create(order_items)

        return order

    def get_seller_orders_by_id(
        self, seller_id: int, filters: dict = {}
    ) -> QuerySet[Order]:
        orders = (
            self.filter(orderitem__product__seller_id=seller_id)
            .annotate(
                seller_total_amount=Sum(
                    F("orderitem__product__price") * F("orderitem__quantity")
                )
            )
            .distinct()
        )
        return self.FilterSet(filters, orders).qs
