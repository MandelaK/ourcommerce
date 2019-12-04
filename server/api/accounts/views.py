from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegisterUserAPIView(CreateAPIView):
    """
    API View for handling User Registration
    """

    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST request for User Login
        """
        payload = request.data

        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {"message": "User successfully created."}

        return Response(response, status=status.HTTP_201_CREATED)
