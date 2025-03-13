from django.db import models
from django.contrib.auth import get_user_model

from apps.utils.models import CreatedAtModel
from apps.products.models import Product

User = get_user_model()


class Order(CreatedAtModel):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PROCESSING = "Processing"
        COMPLETED = "Completed"
        FAILED = "Failed"

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    products = models.ManyToManyField(Product, through="OrderItem")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=StatusChoices, default=StatusChoices.PENDING
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.email} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
