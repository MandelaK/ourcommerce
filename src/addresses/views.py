from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import AddressForm
from billings.models import BillingProfile


def checkout_address_create_view(request):
    """
    This view handles the logic for creating and saving
    billing and shipping addresses
    """
    form = AddressForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    context = {
        "form": form
    }

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(
            request)
        if billing_profile:
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get(
                'address_type', 'shipping')
            instance.save()

        else:
            print("Error with billing profile")
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        return redirect('cart:checkout')

    return render(request, 'cart:checkout', context)
