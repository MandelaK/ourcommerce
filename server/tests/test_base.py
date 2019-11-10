from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase, APIRequestFactory

from tests.factories.accounts_factory import GuestEmailFactory, UserFactory


fake = Faker()

class TestBase(TestCase):
    """
    This class contains the default setup for most tests
    """

    def setUp(self):
        """
        Initialize common reusable test data
        """

        self.guest_email_account1 = GuestEmailFactory.create(
            email='guest1@email.com')

        self.test_user1 = UserFactory.create(
            email='test@user.one'
        )

        self.test_user1_login_data = {
            'email': 'test@user.one',
            'password': 'defaultpassword'
        }

        self.user_registration_data = {
            'username': 'fakedata1',
            'password': 'defaultpassword',
            'confirm_password': 'defaultpassword',
            'email': 'fake@test.data1'
        }


class TestAPIBase(APITestCase):
    """
    This contains the test setup for most API tests
    """

    def setUp(self):
        """
        Set up testing data
        """

        self.api_account_register_url = reverse('api-auth:register')
        self.account_register_url = reverse('accounts:register')
        self.account_login_url = reverse('accounts:login')
        self.guest_register_url = reverse('accounts:register_guest')
        self.logout_url = reverse('accounts:logout')

        self.user_registration_data = {
            'username': 'fakedata1',
            'password': 'defaultpassword',
            'confirm_password': 'defaultpassword',
            'email': 'fake@test.data1'
        }

        self.factory = APIRequestFactory()

        self.test_user1 = UserFactory.create(
            email='test@user.one'
        )

        self.test_user1_login_data = {
            'email': 'test@user.one',
            'password': 'defaultpassword'
        }

        self.guest_email_account2_data = {
            'email': 'guest@temp.test'
        }

        self.test_user_registration_data = {
            'email': 'random@user1.test',
            'username': 'randomuse42',
            'password': 'defaultpassword',
            'confirm_password': 'defaultpassword'
        }


# class FormTestBase(LiveServerTestCase):
#     """
#     The base class that contains setups for testing forms
#     """

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
