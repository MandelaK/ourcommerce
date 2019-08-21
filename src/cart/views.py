from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product
from orders.models import Order


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
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:cart")


def checkout(request):
    """
    View for handling checkout logic
    """
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:cart")
    else:
        order_obj, order_created = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "cart/checkout.html", {"object": order_obj, })
