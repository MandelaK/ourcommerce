from django.db import models

from billings.models import BillingProfile


class Address(models.Model):
    """
    Model for the Addresses
    """

    ADDRESS_TYPES = (("billing", "Billing"), ("shipping", "Shipping"))

    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, default="Kenya")
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.address_type.title()} Address for {self.billing_profile}"

    def get_address(self):
        """
        Return the address in an unambiguous human-readable format
        """

        return "{}\n{}\n{},\n{},\n{}".format(
            self.address_line_1, self.city, self.state, self.postal_code, self.country
        )
