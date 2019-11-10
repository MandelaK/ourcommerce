from rest_framework import status
# TODO: Is there a way to include middleware in my TestCase to avoid repetition?
from django.contrib.sessions.middleware import SessionMiddleware

# TODO use the TestBase class instead
from tests.test_base import TestAPIBase
from accounts.views import login_page, guest_register_page, register_page


class LoginPageTest(TestAPIBase):
    """
    Contains tests for the login_page view
    """

    def test_that_registered_users_can_log_in(self):
        """
        Registered users should be able to log in if they provide valid credentials
        """
        # TODO: Test url user is redirected to

        request = self.factory.post(self.account_login_url, self.test_user1_login_data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        response = login_page(request)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_that_registered_users_can_only_log_in_with_valid_credentials(self):
        """
        If a user provides invalid credentials, the page shouldl simply reload with
        an error message
        """
        # TODO: Make this functional test

        data = self.test_user1_login_data.copy()
        data['password'] = 'wrongpassword'
        request = self.factory.post(self.account_login_url, data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        response = login_page(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_users_who_log_in_with_redirect_link_get_successfully_redirected(self):
        """
        If a user logs in and they have a url they were supposed to be redirected to,
        they should be succesfully redirected after login
        """
        # TODO: Test url user is redirected to

        data = self.test_user1_login_data.copy()
        data['next'] = '/cart/'
        request = self.factory.post(self.account_login_url, data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        response = login_page(request)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_that_login_attempts_fail_if_login_form_is_invalid(self):
        """
        The login from must be properly structured before users can be logged in. If it is not
        correctly structured, the page should reload with the appropriate error message
        """
        # TODO: Make this functional test

        data = self.test_user1_login_data.copy()
        data.pop('password')
        request = self.factory.post(self.account_login_url, data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        response = login_page(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GuestRegisterPageTest(TestAPIBase):
    """
    Contains tests for guest registration view
    """

    def test_that_guest_users_can_register(self):
        """
        Guest users should be able to register by supplying their email address
        """
        # TODO: Test actual url redirected to

        request = self.factory.post(self.guest_register_url, self.guest_email_account2_data)
        middleware = SessionMiddleware()
        middleware.process_request(request)

        response = guest_register_page(request)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_that_guest_registration_form_must_be_valid_before_guest_accounts_can_be_created(self):
        """
        The guest registration form must be validated before we can proceed to create
        guest email accounts
        """
        # TODO: Make this functional test

        request = self.factory.post(self.guest_register_url, {})
        middleware = SessionMiddleware()
        middleware.process_request(request)

        response = guest_register_page(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_guest_users_are_redirected_to_next_url_after_succesful_registration(self):
        """
        Guest users should be able to register by supplying their email address. If they were to be
        redirected to a specific url after succesful registration, they should be redirected
        """
        data = self.guest_email_account2_data.copy()
        data['next'] = '/checkout/'
        request = self.factory.post(self.guest_register_url, data)
        middleware = SessionMiddleware()
        middleware.process_request(request)

        response = guest_register_page(request)

        # TODO: Test actual url user is redirected to

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class RegisterPageTest(TestAPIBase):
    """
    Test the registration page
    """

    def test_that_users_can_succesfully_register_if_they_enter_valid_data(self):
        """
        Users should be able to register provided they enter valid information
        """
        request = self.factory.post(self.account_register_url, self.test_user_registration_data)

        middleware = SessionMiddleware()
        middleware.process_request(request)

        response = register_page(request)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_that_users_cannot_register_if_their_registration_details_are_invalid(self):
        """
        If there are any errors when signing up, the page will reload
        """
        # TODO: Make this functional test

        data = self.test_user_registration_data.copy()
        data['confirm_password'] = 'LOL!'
        request = self.factory.post(self.account_register_url, data)

        middleware = SessionMiddleware()
        middleware.process_request(request)

        response = register_page(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
