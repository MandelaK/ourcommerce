from django.contrib.auth import get_user_model

from tests.test_base import TestBase
from accounts.forms import RegisterForm


User = get_user_model()


class RegisterFormTestCase(TestBase):
    """
    Contains tests for the functionality of the register form
    """
    def test_that_emails_are_properly_cleaned_if_they_are_not_unique(self):
        """
        Users should be allowed to use only unique emails
        """

        data = self.user_registration_data
        email = User.objects.first().email
        data['email'] = email

        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors, {'email': ['A user with this email exists already']})

    def test_that_passwords_must_match_in_registration_form(self):
        """
        The user must enter two matching passwords when they are creating their account.
        """

        data = self.user_registration_data
        data['confirm_password'] = 'thisissodefinitelywrong'

        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords must match!', form.errors.get('__all__'))
