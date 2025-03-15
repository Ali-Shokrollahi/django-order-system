from apps.products.repositories import ProductRepository
from apps.orders.repositories import OrderRepository


class SellerService:
    product_repository = ProductRepository()
    order_repository = OrderRepository()

    def get_seller_products(self, seller_id):
        return self.product_repository.get_products_by_seller(seller_id)

    def get_seller_orders(self, seller_id, filters: dict = {}):
        return self.order_repository.get_seller_orders_by_id(seller_id, filters)
