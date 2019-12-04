from django.urls import path
from products.views import (
    ProductListView,
    ProductDetailView,
    ProductFeaturedListView,
    ProductFeaturedDetailView,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="list_products"),
    path("<slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("f/featured/", ProductFeaturedListView.as_view(), name="featured_products"),
    path(
        "featured/<pk>/", ProductFeaturedDetailView.as_view(), name="featured_product"
    ),
]
