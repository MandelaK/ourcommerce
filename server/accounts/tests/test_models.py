from accounts.models import CustomUser
from tests.test_base import TestBase


class TestGuestEmailModel(TestBase):
    """
    Contain tests for the GuestEmail Model
    """

    def test_that_we_get_back_proper_representation(self):
        """
        We should get back the proper string representation
        for all initialized GuestEmail models
        """

        self.assertEqual(str(self.guest_email_account1), 'guest1@email.com')


class TestUserManager(TestBase):
    """
    Test the User Manager methods
    """

    def test_that_we_can_get_existing_users_with_the_get_or_create_call(self):
        """
        We should be able to get existing new users or create new ones
        if we don't get then from the passed arguments
        """

        user, created = CustomUser.objects.get_or_create(email=self.test_user1.email)

        self.assertFalse(created)
        self.assertEqual(user, self.test_user1)

    def test_that_we_can_create_users_if_none_exist_with_get_or_create_call(self):
        """
        If no users exist with the passed credentials, we should be able to create them
        and save their password too
        """

        user, created = CustomUser.objects.get_or_create(
            email='nonexistent@user.test', username='nonexistent', password='defaultpassword'
        )

        self.assertTrue(created)
        # the username field might change, so we simply ensure that
        # the proper representation is returned
        self.assertEqual(str(user), user.get_username())
