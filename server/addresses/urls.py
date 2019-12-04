from django.urls import path

from .views import checkout_address_create_view, checkout_address_reuse_view


urlpatterns = [
    path("", checkout_address_create_view, name="address"),
    path("reuse/", checkout_address_reuse_view, name="reuse"),
]
