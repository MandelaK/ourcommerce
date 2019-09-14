from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Cart
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from billings.models import BillingProfile
from products.models import Product
from orders.models import Order
from addresses.forms import AddressForm
from addresses.models import Address


def cart_detail_api_view(request):
    """
    API view for the cart view
    """

    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [
        {
            "id": x.id,
            "name": x.title,
            "price": x.price,
            "description": x.description,
            "url": x.get_absolute_url()
        } for x in cart_obj.products.all()
    ]
    data = {
        "products": products,
        "subtotal": cart_obj.subtotal,
        "total": cart_obj.total
    }
    return JsonResponse(data)


def cart_home(request):
    """
    Endpoint for retreiving and/or creating the
    user's cart
    """
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "cart/home.html", {"cart": cart_obj})


def cart_update(request):
    """
    View for updating the cart
    """
    product_id = request.POST.get('product_id')
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            product_added = True
        cart_item_count = cart_obj.products.count()
        request.session['cart_items'] = cart_item_count
        if request.is_ajax:
            json_data = {
                "added": product_added,
                # we send back the cart item count too
                "cart_item_count": cart_item_count
            }
            return JsonResponse(json_data)
    return redirect("cart:cart")


def checkout(request):
    """
    View for handling checkout logic
    """
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:cart")
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_profile, created = BillingProfile.objects.new_or_get(request)

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(
                billing_profile=billing_profile)
        order_obj, order_created = Order.objects.new_or_get(
            billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(
                pk=shipping_address_id)
            order_obj.save()
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(
                pk=billing_address_id)
            order_obj.save()
            del request.session["billing_address_id"]
    if request.method == "POST":
        is_done = order_obj.check_order()
        if is_done:
            order_obj.mark_done()
            request.session["cart_items"] = 0
            del request.session["cart_id"]
            return redirect("cart:done")
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs
    }
    return render(request, "cart/checkout.html", context=context)


def checkout_done_view(request):
    """
    This view handles logic related to completing the checkout process
    """

    return render(request, "cart/checkout-done.html", {})


# TODO: Allow users to change addresses during checkout
