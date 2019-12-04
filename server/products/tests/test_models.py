from tests.test_base import TestBase

from products.models import Product
from tests.factories.products_factory import ProductFactory

class ProductModelTest(TestBase):
    """
    Contain tests for the Product model.
    """

    def test_that_we_can_create_products(self):
        product = Product.objects.create(title="TestProduct", description="Test Product", price=34.4)

        self.assertIsInstance(product, Product)
        self.assertEqual(product.title, "TestProduct")


class ProductQuerySetTest(TestBase):
    """
    Test the custom Products queryset.
    """

    def test_that_we_can_search_products_by_any_field(self):
        ProductFactory.create(title="testing")
        # we search for a product by price
        products = Product.objects.search(234)

        self.assertTrue(products.exists())

        # search by title
        
        products_title = Product.objects.search("testing")
        self.assertTrue(products_title.exists())

    def test_that_product_instances_have_valid_absolute_urls(self):
        self.assertEqual(self.product1.get_absolute_url(), f'/products/{self.product1.slug}/')

    def test_that_product_instances_have_proper_string_represetation(self):
        self.assertEqual(str(self.product1), self.product1.title)
