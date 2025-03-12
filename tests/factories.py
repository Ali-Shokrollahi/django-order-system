from uuid import uuid4
from decimal import Decimal
import factory
from django.contrib.auth import get_user_model
from apps.products.models import Product

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
