from django.db import models
from django.db.models.signals import pre_save

from products.utils import unique_slug_generator


class ProductQuerySet(models.query.QuerySet):
    """Implement custom queryset for Product model"""

    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    """Custom manager for the Products class"""

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def featured(self):
        return self.get_queryset().featured()

    def all(self):
        """Only return active objects"""
        return self.get_queryset().active()


class Product(models.Model):
    """Define product model"""

    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=3, max_digits=13)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return f"{self.slug}/"

    def __str__(self):
        return self.title


def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save, Product)
