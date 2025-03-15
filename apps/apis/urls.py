from django.urls import path, include


urlpatterns = [
    path("accounts/", include("apps.accounts.urls"), name="accounts"),
    path("products/", include("apps.products.urls"), name="products"),
    path("orders/", include("apps.orders.urls"), name="orders"),
    path("sellers/", include("apps.sellers.urls"), name="sellers"),
]
