from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class GuestEmail(models.Model):
    """
    Define the fields for guest users
    """
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager):
    """
    Manager for handling User model
    """

    def get_or_create(self, **kwargs):
        """
        Get or create a new user instance. If multiple users instances are found,
        we return the first instance
        """
        try:
            password = kwargs.get('password')
            if password:
                kwargs.pop('password')
            user, created = super().get_or_create(**kwargs)
            if created:
                user.set_password(password)
                user.save()
                return user, created
            return user, created
        except self.model.MultipleObjectsReturned:
            queryset = self.model.objects.filter(**kwargs)
            # TODO: Find solution to what happens to duplicate accounts already saved in DB
            return queryset.first(), False


class CustomUser(AbstractBaseUser):
    """
    Custom Model to handle User instance
    """

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()
