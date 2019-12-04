from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware

from tests.test_base import TestBase
from products.views import ProductDetailView

class ProductDetailViewTest(TestBase):
    """
    Test the product detail view.
    """

    def test_that_the_cart_is_passed_to_the_session_key(self):

        request = self.factory.get(reverse("products:product_detail", args=[self.product1.slug]))

        middleware = SessionMiddleware()
        middleware.process_request(request)

        view = ProductDetailView.as_view()
        request.user = self.test_user1

        response = view(request, slug=self.product1.slug)

        self.assertTrue(response.context_data.get("cart"))
