from celery import chain
from django.db import transaction
from apps.utils.exceptions import ResourceNotFoundException
from apps.orders.models import Order
from apps.products.repositories import ProductRepository

from .repositories import InvoiceRepository, OrderRepository
from .tasks import generate_and_save_invoice, send_order_confirmation_email


class OrderService:
    order_repository = OrderRepository()
    product_repository = ProductRepository()
    invoice_repository = InvoiceRepository()

    @transaction.atomic
    def create_order(self, customer, products_data: list[dict]) -> Order:
        """
        Create an order with total amount calculation, fetching products via ProductRepository.
        products_data: List of dicts with 'product_id' and 'quantity'.
        """
        product_dict = {
            str(item["product_id"]): item["quantity"] for item in products_data
        }
        product_ids = list(product_dict.keys())

        products = self.product_repository.get_products_by_ids(
            product_ids, fields=["id", "price"]
        )
        products_by_id = {str(product.id): product for product in products}

        # Ensure all products exist
        missing = set(product_dict.keys()) - products_by_id.keys()
        if missing:
            raise ResourceNotFoundException(
                resource_name="Product", extra={"missing_products": list(missing)}
            )

        total_amount = sum(
            float(product.price) * product_dict[pid]
            for pid, product in products_by_id.items()
        )

        order = self.order_repository.create_order(
            customer=customer, products_data=product_dict, total_amount=total_amount
        )

        chain(
            generate_and_save_invoice.s(order.id),
            send_order_confirmation_email.si(order.id, customer.email),
        )()

        return order

    def get_customer_orders(self, customer_id: int, filters: dict = {}):
        return self.order_repository.get_customer_orders_by_id(
            customer_id, filters=filters
        )

    def get_order_details(self, order_id: int):
        order = self.order_repository.get_order_and_order_items_by_id(order_id)
        if not order:
            raise ResourceNotFoundException(resource_name="Order)")
        return order

    def get_order_by_id(self, order_id: int):
        order = self.order_repository.get(pk=order_id)
        if not order:
            raise ResourceNotFoundException(resource_name="Order")
        return order

    def get_order_invoice(self, order_id: int):
        invoice = self.invoice_repository.get_invoice_by_order_id(order_id)
        if not invoice:
            raise ResourceNotFoundException(resource_name="Invoice")
        return invoice
