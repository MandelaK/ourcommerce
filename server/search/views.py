from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView

from products.models import Product

# Create your views here.


class SearchProductView(ListView):
    """
    Define the methods for handling the search functionality
    """

    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get("q")
        if query:
            return Product.objects.search(query)
        return Product.objects.featured()
