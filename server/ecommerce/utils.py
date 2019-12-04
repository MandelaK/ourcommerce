import string
import random

from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):
    """Create a new unique slug"""

    if new_slug is not None:
        unique_slug = new_slug
    else:
        unique_slug = slugify(instance.title)

    extension = 1

    CLASS = instance.__class__
    while CLASS._default_manager.filter(**{"slug": unique_slug}).exists():
        unique_slug = f"{unique_slug}-{extension}"
        extension += 1

    return unique_slug


def random_string_generator(size=15, chars=string.ascii_uppercase + string.digits):
    """Generate a random string with a length of `size`"""
    return "".join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    """Generate a new random and unique order_id"""

    new_order_id = random_string_generator()

    CLASS = instance.__class__
    while CLASS._default_manager.filter(**{"order_id": new_order_id}).exists():
        return unique_order_id_generator(instance)

    return new_order_id
