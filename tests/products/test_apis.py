import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestProductCreateApi:
    """Tests for ProductCreateApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request
        self.url = reverse("product_create")

    def test_create_product_success(self, seller, create_product_payload):
        """Test seller can create a product."""
        response = self.request("post", self.url, create_product_payload, user=seller)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == create_product_payload["name"]
        assert data["price"] == create_product_payload["price"]

    def test_create_product_non_seller_denied(self, customer, create_product_payload):
        """Test non-seller gets 403."""
        response = self.request("post", self.url, create_product_payload, user=customer)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_unauthenticated(self, create_product_payload):
        """Test unauthenticated user gets 401."""
        response = self.request("post", self.url, create_product_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProductListApi:
    """Tests for ProductListApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request
        self.url = reverse("product_list")

    def test_list_products_success(self, product_factory):
        """Test listing products with pagination."""
        products = product_factory.create_batch(2)
        response = self.request("get", self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 2
        assert data["data"][0]["id"] == str(products[0].id)

    def test_list_products_with_filters(self, seller, product_factory):
        """Test filtering products."""
        product_factory.create(name="Laptop", price=500, seller=seller)
        product_factory.create(name="Phone", price=1000, seller=seller)
        query_params = {"search": "lap", "limit": 1}
        response = self.request("get", self.url, query_params=query_params)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "Laptop"


@pytest.mark.django_db
class TestProductDetailApi:
    """Tests for ProductDetailApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request

    def test_get_product_detail_success(self, product):
        """Test retrieving product details."""
        url = reverse("product_detail", args=[product.id])
        response = self.request("get", url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(product.id)
        assert data["name"] == product.name
        assert data["description"] == product.description
        assert data["seller"]["email"] == product.seller.email


@pytest.mark.django_db
class TestProductUpdateApi:
    """Tests for ProductUpdateApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request

    def test_update_product_success(self, seller, product, update_product_payload):
        """Test seller can update their product."""
        url = reverse("product_update", args=[product.id])
        response = self.request("patch", url, update_product_payload, user=seller)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_product_payload["name"]
        assert data["price"] == update_product_payload["price"]

    def test_update_product_non_owner_denied(
        self, customer, product, update_product_payload
    ):
        """Test non-owner gets 403."""
        url = reverse("product_update", args=[product.id])
        response = self.request("patch", url, update_product_payload, user=customer)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_product_unauthenticated(self, product, update_product_payload):
        """Test unauthenticated user gets 401."""
        url = reverse("product_update", args=[product.id])
        response = self.request("put", url, update_product_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProductDeleteApi:
    """Tests for ProductDeleteApi view."""

    @pytest.fixture(autouse=True)
    def setup(self, api_request):
        self.request = api_request

    def test_delete_product_success(self, seller, product):
        """Test seller can delete their product."""
        url = reverse("product_delete", args=[product.id])
        response = self.request("delete", url, user=seller)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_product_non_owner_denied(self, customer, product):
        """Test non-owner gets 403."""
        url = reverse("product_delete", args=[product.id])
        response = self.request("delete", url, user=customer)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_unauthenticated(self, product):
        """Test unauthenticated user gets 401."""
        url = reverse("product_delete", args=[product.id])
        response = self.request("delete", url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
