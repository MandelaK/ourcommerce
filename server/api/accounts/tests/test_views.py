from rest_framework import status
from django.contrib.auth import get_user_model

from tests.test_base import TestAPIBase


class TestRegisterUserAPIView(TestAPIBase):
    """
    Test API view that handles user registration
    """

    def test_users_can_register_from_api_view(self):
        """
        Users should be able to register new accounts
        from the API view after submitting valid data
        """

        res = self.client.post(self.api_account_register_url,
                               self.user_registration_data,
                               format='json'
                               )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data.get('message'), 'User successfully created.')

        # assert user is created in DB
        created_user = get_user_model().objects.get(
            email=self.user_registration_data.get('email')
            )
        self.assertEqual(str(created_user), self.user_registration_data.get('email'))
