from django_filters import FilterSet
from apps.orders.models import Order
from apps.products.repositories import ProductRepository
from apps.orders.repositories import OrderRepository


class SellerService:
    product_repository = ProductRepository()
    order_repository = OrderRepository()

    class OrderFilterSet(FilterSet):
        class Meta:
            model = Order
            fields = ["status"]

    def get_seller_products(self, seller_id):
        return self.product_repository.get_products_by_seller(seller_id)

    def get_seller_orders(self, seller_id, filters: dict = {}):
        orders = self.order_repository.get_orders_by_seller(seller_id)
        return self.OrderFilterSet(filters, orders).qs
