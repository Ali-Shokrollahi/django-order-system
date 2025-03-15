from django.urls import path
from .apis import OrderCreateApi, OrderListApi, OrderDetailApi, OrderInvoiceApi

urlpatterns = [
    path("create/", OrderCreateApi.as_view(), name="order_create"),
    path("", OrderListApi.as_view(), name="order_list"),
    path("<int:order_id>/", OrderDetailApi.as_view(), name="order_detail"),
    path("<int:order_id>/invoice/", OrderInvoiceApi.as_view(), name="order_invoice")
]
