from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class that handles the serialization of user
    data during registration
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    confirm_password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'confirm_password']

    def validate(self, data):
        """
        Validate and ensure that passwords are valid and that they match
        """

        try:
            password_validation.validate_password(data.get('password'))
            def do_passwords_match(
                password1, password2): return password1 == password2
            match = do_passwords_match(
                data.get('password'), data.get('confirm_password'))
        except ValidationError as e:
            raise exceptions.ValidationError({
                "password": e.messages
            })

        if not match:
            raise exceptions.ValidationError({
                "confirm_password": "Your passwords do not match"})
        return data

    def create(self, validated_data):
        """
        Method that actually creates users
        """
        validated_data.pop('confirm_password')
        email, password = validated_data.get(
            'email'), validated_data.get('password'),
        try:
            user, created = User.objects.get_or_create(
                email=email, password=password)

            if not created:
                raise exceptions.ValidationError({
                    "user": ("A user is already registered with those credentials. "
                             "You can either log in or try registering with different cretentials."
                             )
                })
            return user

        except IntegrityError:
            raise exceptions.ValidationError({
                "user": ("A user is already registered with those credentials. "
                         "You can either log in or try registering with different "
                         "cretentials."
                         )
            })
