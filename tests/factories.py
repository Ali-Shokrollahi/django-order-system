from uuid import uuid4
from decimal import Decimal
import factory
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.orders.models import Order, OrderItem

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")

    role = User.RoleChoices.CUSTOMER
    is_active = False
    is_verified = False

    @factory.lazy_attribute
    def password(self):
        return "Test@1pass"

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.set_password(instance.password)
            instance.save()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    id = factory.LazyFunction(uuid4)
    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("text")
    price = Decimal("99.99")
    seller = factory.SubFactory(UserFactory)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory, role=User.RoleChoices.CUSTOMER)
    total_amount = Decimal("199.99")
    status = Order.StatusChoices.PENDING

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1