from factory.django import DjangoModelFactory, Password
from factory.faker import Faker

from tests.website.models import User


class UserFactory(DjangoModelFactory[User]):
    username = Faker('name')
    password = Password('local')
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = User
