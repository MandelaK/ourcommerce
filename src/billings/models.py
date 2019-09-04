from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    """
    Model manager for the Billing Profile class
    """

    def new_or_get(self, request):
        """
        Get an existing billing profile or create a new one if it does not exist
        """
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            # TODO check if the user has an email address
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        elif guest_email_id:
            guest_email_obj = GuestEmail.objects.get(pk=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:  # TODO what do we do if the above checks don't happen?
            pass

        return obj, created


class BillingProfile(models.Model):
    """
    Describe the fields for a billing profile
    """
    user = models.OneToOneField(User, null=True,
                                blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # customer_id on Stripe, etc

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    """Create a billing profile for every new user"""
    if created and instance.email:
        BillingProfile.objects.get_or_create(
            user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
