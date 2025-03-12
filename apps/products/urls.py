from django.urls import path
from .apis import ProductCreateApi, ProductListApi, ProductDetailApi, ProductUpdateApi, ProductDeleteApi

urlpatterns = [
    path("", ProductListApi.as_view(), name="product_list"),
    path("create/", ProductCreateApi.as_view(), name="product_create"),
    path("<uuid:product_id>/", ProductDetailApi.as_view(), name="product_detail"),
    path("<uuid:product_id>/update/", ProductUpdateApi.as_view(), name="product_update"),
    path("<uuid:product_id>/delete/", ProductDeleteApi.as_view(), name="product_delete"),
]