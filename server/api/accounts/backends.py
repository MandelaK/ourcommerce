from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Define the Authentication Backend for REST API Endpoints
    """

    auth_header_prefix = "Bearer".lower()

    def authenticate(self, request):
        """
        This method will be called against every endpoint

        Return None to indicate that authentication was not
        successful

        Return tuple of `(user, token)` if authentication is
        successful

        Raise `AuthenticationFailed` errors whenever an error
        is encountered
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header:
            return None

        if not len(auth_header) == 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != self.auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        This method is called to ensure that user credentials
        are correct
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                detail="Your session has expired. Please log in again.", code="invalid"
            )

        try:
            user = get_user_model().objects.get(pk=payload.get("id"))
            if not user.is_active:
                raise exceptions.AuthenticationFailed(
                    "This user has been deactived.", code="invalid"
                )
        except Exception as e:
            raise exceptions.AuthenticationFailed(detail=e, code="invalid")

        return (user, token)
