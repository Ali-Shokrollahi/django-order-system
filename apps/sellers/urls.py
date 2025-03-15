from django.urls import path
from .apis import SellerProductListApi, SellerOrderListApi

urlpatterns = [
    path("products/", SellerProductListApi.as_view(), name="seller_product_list"),
    path("orders/", SellerOrderListApi.as_view(), name="seller_order_list"),
]
