import pytest

@pytest.fixture
def seller_service():
    from apps.sellers.services import SellerService

    return SellerService()



