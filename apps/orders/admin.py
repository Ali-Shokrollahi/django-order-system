from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "status")
    list_filter = ("status", "created_at")

    ordering = ("-created_at",)

    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
    list_filter = "order"

    ordering = ("-order",)
