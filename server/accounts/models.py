from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


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

        password = kwargs.get('password')
        if password:
            kwargs.pop('password')
        kwargs['email'] = self.normalize_email(kwargs['email'])
        user, created = super().get_or_create(**kwargs)
        if created:
            user.set_password(password)
            user.save()

        return user, created

    def create_user(self, email=None, password=None, **kwargs):
        if not email:
            raise TypeError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), password=password, username=email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email=None, password=None, **kwargs):
        if not password:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(email=email, password=password, is_superuser=True, is_staff=True, **kwargs)
        return user



class CustomUser(AbstractUser):
    """
    Custom Model to handle User instance
    """

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Return the string representation of CustomUser
        """

        return self.get_username()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name.title()} {self.last_name.title()}"
        return self.get_username()

    def get_short_name(self):
        return self.get_username()
