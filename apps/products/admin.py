from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller")
    list_filter = ("seller", "created_at")

    search_fields = ("name",)

    ordering = ("-created_at",)

    readonly_fields = ("id", "created_at", "updated_at")
