import uuid
from django.db import models

from apps.utils.models import TimeStampModel


class Product(TimeStampModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=["seller"], name="idx_product_seller"),
            models.Index(fields=["name"], name="idx_product_name"),
        ]

    def __str__(self):
        return self.name
