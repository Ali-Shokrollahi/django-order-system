import pytest
from uuid import uuid4
from apps.utils.exceptions import ResourceNotFoundException


@pytest.mark.django_db
class TestProductService:
    """Tests for ProductService class."""

    @pytest.fixture(autouse=True)
    def setup(self, product_service):
        self.service = product_service

    def test_create_product_success(self, seller, create_product_payload):
        """Test creating a new product successfully."""

        product = self.service.create_product(**create_product_payload, seller=seller)

        assert product.name == create_product_payload["name"]
        assert product.description == create_product_payload["description"]
        assert product.price == create_product_payload["price"]
        assert product.seller == seller
        assert str(product.id)

    def test_get_all_products_no_filters(self, product_factory):
        """Test retrieving all products without filters."""
        created_products = product_factory.create_batch(2)
        products = self.service.get_all_products()
        assert created_products[0] in products
        assert products.count() == 2

    def test_get_all_products_with_filters(self, seller, product_factory):
        """Test filtering products by name, price, and seller."""
        product1 = product_factory.create(name="Laptop", price=500, seller=seller)
        product2 = product_factory.create(name="Phone", price=1000, seller=seller)

        # Filter by name
        filters = {"search": "lap"}
        products = self.service.get_all_products(filters)
        assert product1 in products
        assert product2 not in products

        # Filter by price range
        filters = {"price_min": 600, "price_max": 1200}
        products = self.service.get_all_products(filters)
        assert product2 in products
        assert product1 not in products

        # Filter by seller
        filters = {"seller": seller.id}
        products = self.service.get_all_products(filters)
        assert products.count() == 2

    def test_get_product_by_id_success(self, product):
        """Test retrieving a product by ID."""
        retrieved_product = self.service.get_product_by_id(product.id)
        assert retrieved_product == product

    def test_get_product_by_id_not_found(self):
        """Test retrieving a non-existent product raises an exception."""
        with pytest.raises(ResourceNotFoundException) as exc:
            self.service.get_product_by_id(uuid4())
        assert "Product not found" in str(exc.value)

    def test_update_product_success(self, product, update_product_payload):
        """Test updating a product’s attributes."""
        updated_product = self.service.update_product(product, **update_product_payload)

        product.refresh_from_db()
        assert product.name == update_product_payload["name"]
        assert updated_product == product

    def test_delete_product_success(self, product):
        """Test deleting a product."""
        self.service.delete_product(product)
        with pytest.raises(ResourceNotFoundException):
            self.service.get_product_by_id(product.id)
