from django import forms

from .models import Address


AddressForm = forms.modelform_factory(
    Address, exclude=("billing_profile", "address_type",)
)
