from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    """Manager for the Cart Object"""

    def new_or_get(self, request):
        """
        Return a new cart object or create one based
        on the request
        """
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.exists():
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        """Create a new cart object"""
        if user and user.is_authenticated:
            user_obj = user
        else:
            user_obj = None
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    """Defines fields for the Cart model"""

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    """
    WHenever the Products are updated for this cart, before we save the cart,
    we get the total price of all the products in the cart.
    """
    ACTIONS = ["post_add", "post_remove", "post_clear"]
    if action in ACTIONS:
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price

        instance.subtotal = total
        instance.save()


# whenever the Products, ie sender, are updated for this cart, we update the subtotal
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    """
    Whenever this cart is saved, we calculate the total price, including any additional
    Fees
    """
    if instance.subtotal > 0:
        instance.total = instance.subtotal
    else:
        instance.total = 0.00


# before we save the cart, we update the total
pre_save.connect(pre_save_cart_receiver, sender=Cart)
