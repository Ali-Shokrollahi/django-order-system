from uuid import uuid4
import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestOrderCreateApi:
    """Tests for OrderCreateApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request
        self.url = reverse("order_create")

    def test_create_order_success(self, customer, create_order_payload):
        """Test customer can create an order."""
        response = self.request("post", self.url, create_order_payload, user=customer)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_order_unauthenticated(self, create_order_payload):
        """Test unauthenticated user gets 401."""
        response = self.request("post", self.url, create_order_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_non_existent_product(self, customer):
        """Test non-existent product returns 404."""
        payload = {"products_data": [{"product_id": str(uuid4()), "quantity": 1}]}
        response = self.request("post", self.url, payload, user=customer)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product not found" in response.json()["message"]

    def test_create_order_empty_products(self, customer):
        """Test empty products list returns 400."""
        payload = {"products_data": []}
        response = self.request("post", self.url, payload, user=customer)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
