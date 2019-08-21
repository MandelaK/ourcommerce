import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from cart.models import Cart
from ecommerce.utils import unique_order_id_generator


SHIPPING_DEFAULT = 100.0


class Order(models.Model):
    """
    Define the fields for the Orders table
    """

    ORDER_STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('refunded', 'Refunded')
    )

    order_id = models.CharField(max_length=120, blank=True, unique=True)
    # billing_profile =
    # shipping_address =
    # billing_address =
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(
        default=SHIPPING_DEFAULT, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.order_id)

    def update_total(self):
        """
        Update the total price for all the products in the cart
        """
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        total = math.fsum([cart_total, shipping_total])
        formated_total = format(total, '.2f')
        self.total = formated_total
        self.save()
        return self.total


def pre_save_order_receiver(sender, instance, *args, **kwargs):
    """
    Before we save the Order, we need to set its unique order_id
    """
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_order_receiver, sender=Order)


def post_save_cart_receiver(sender, instance, created, *args, **kwargs):
    """
    Whenever the Cart is saved, and not created, we update the total
    """
    if not created:
        cart_total = instance.total
        cart_id = instance.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists():
            # TODO fix redundancy of having more than one order
            # for the same cart
            # we will only update the first instance
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_receiver, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    """Whenever an order is created, we simply update the total"""
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
