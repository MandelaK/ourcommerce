from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cart.models import Cart
from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(
    #         *args, **kwargs)
    #     print(context)
    #     return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj = Cart.objects.new_or_get(self.request)[0]
        context["cart"] = cart_obj
        return context


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.featured()


class ProductFeaturedListView(ListView):
    queryset = Product.objects.featured()
