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

        self.assertEqual(str(self.guest_email_account1), "guest1@email.com")


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
            email="nonexistent@user.test",
            username="nonexistent",
            password="defaultpassword",
        )

        self.assertTrue(created)
        # the username field might change, so we simply ensure that
        # the proper representation is returned
        self.assertEqual(str(user), user.get_username())

    def test_that_users_must_be_created_with_an_email(self):
        """
        User accounts cannot be created if no email is supplied.
        """

        with self.assertRaises(TypeError) as exc:
            CustomUser.objects.create_user(password="defaultpassword")

        self.assertEqual(str(exc.exception), "Users must have an email address.")

    def test_that_users_are_created_if_all_necessary_arguments_are_provided(self):
        user = CustomUser.objects.create_user(
            email="test@mail.com", password="password"
        )

        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, "test@mail.com")

    def test_that_superusers_cannot_be_created_without_passwords(self):
        with self.assertRaises(TypeError) as exc:
            CustomUser.objects.create_superuser(email="test@superuser.com")

        self.assertEqual(str(exc.exception), "Superusers must have a password.")

    def test_that_superusers_are_created_if_all_fields_are_provided(self):
        """
        We should be able to create superusers provided that we pass all required fields.
        """

        superuser = CustomUser.objects.create_superuser(
            email="superuser@mail.com", password="superuserpassword"
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertIsInstance(superuser, CustomUser)

    def test_that_users_get_full_names_if_first_and_last_name_present(self):
        user = CustomUser.objects.create_user(
            email="first@user.test",
            password="password",
            first_name="first",
            last_name="last",
        )

        self.assertEqual(user.get_full_name(), "First Last")

    def test_that_users_get_full_names_if_no_first_and_last_names(self):
        self.assertEqual(self.test_user1.get_full_name(), "test@user.one")

    def test_that_users_can_get_short_names(self):
        self.assertEqual(self.test_user1.get_short_name(), "test@user.one")
