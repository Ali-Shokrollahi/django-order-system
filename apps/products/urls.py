from django.urls import path
from .apis import ProductCreateApi, ProductListApi

urlpatterns = [
    path("", ProductListApi.as_view(), name="product_list"),
    path("create/", ProductCreateApi.as_view(), name="product_create"),
]