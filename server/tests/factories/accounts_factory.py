"""
This module contains factories to help create dummy data
for different test cases.
"""
from faker import Faker
import factory
from django.contrib.auth import get_user_model

from accounts.models import GuestEmail


fake = Faker()


class UserFactory(factory.DjangoModelFactory):
    """
    This factory will create dummy users and save them
    to the database
    """

    class Meta:
        model = get_user_model()

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    # users are created with the default password of `defaultpassword`
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class GuestEmailFactory(factory.DjangoModelFactory):
    """
    This factory is responsible for creating dummy GuestEmail
    accounts
    """

    class Meta:
        model = GuestEmail

    email = factory.LazyAttribute(lambda _: fake.email())
    timestamp = factory.LazyAttribute(lambda _: fake.time_object())
    timestamp = factory.LazyAttribute(lambda _: fake.time_object())
    active = True
