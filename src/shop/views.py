from django.shortcuts import render  # NOQA: F401
from django.views.generic import DetailView, ListView

from shop.models import Item


class ProductListView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"


class ProductDetailsView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "item"
