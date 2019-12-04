from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Address
from .forms import AddressForm
from billings.models import BillingProfile


def checkout_address_create_view(request):
    """
    This view handles the logic for creating and saving
    billing and shipping addresses
    """
    form = AddressForm(request.POST or None)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    context = {"form": form}

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile:
            address_type = request.POST.get("address_type", "shipping")
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()

            request.session[f"{address_type}_address_id"] = instance.id

        else:
            print("Error with billing profile")
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)

    return render(request, "cart:checkout", context)


def checkout_address_reuse_view(request):
    """
    This view handles the logic for reusing addresses
    that are already saved by the user
    """

    if request.user.is_authenticated:
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None

        if request.method == "POST":
            shipping_address_id = request.POST.get("shipping_address")
            address_type = request.POST.get("address_type", "shipping")
            billing_profile, created = BillingProfile.objects.new_or_get(request)
            if shipping_address_id:
                qs = Address.objects.filter(
                    billing_profile=billing_profile, id=shipping_address_id
                )
                if qs.exists():
                    request.session[f"{address_type}_address_id"] = shipping_address_id

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

    return render(request, "cart:checkout")
