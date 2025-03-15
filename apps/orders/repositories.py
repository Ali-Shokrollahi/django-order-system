from django.db.models import QuerySet, Sum, F
from apps.orders.models import Order, OrderItem
from django.contrib.auth.models import User

from apps.utils.base_repo import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

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

    def get_orders_by_seller(self, seller_id: int) -> QuerySet[Order]:
        return (
            self.filter(orderitem__product__seller_id=seller_id)
            .annotate(
                seller_total_amount=Sum(
                    F("orderitem__product__price") * F("orderitem__quantity")
                )
            )
            .distinct()
        )
