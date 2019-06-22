from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        unique_slug = new_slug
    else:
        unique_slug = slugify(instance.title)

    extension = 1

    CLASS = instance.__class__
    while CLASS._default_manager.filter(**{'slug': unique_slug}).exists():
        unique_slug = f'{unique_slug}-{extension}'
        extension += 1

    return unique_slug
