"""
Methods to create dummy products.
"""

import factory
from faker import Faker

from products.models import Product

fake = Faker()

class ProductFactory(factory.DjangoModelFactory):
    """
    Factory class to create fake products.
    """

    class Meta:
        model = Product
    
    title = fake.word()
    slug = factory.LazyAttribute(lambda _: fake.word())
    description = fake.text()
    price = 23452.54
