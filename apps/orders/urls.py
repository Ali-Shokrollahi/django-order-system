from django.urls import path
from .apis import OrderCreateApi

urlpatterns = [
    path("create/", OrderCreateApi.as_view(), name="order_create"),
]