from django.shortcuts import render
from django.views.generic import ListView, DetailView

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


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.featured()


class ProductFeaturedListView(ListView):
    queryset = Product.objects.featured()
