from django.shortcuts import render  # NOQA: F401
from django.views.generic import TemplateView, ListView
from shop.models import Item


class ProductListView(ListView):
    model = Item
    template_name = "home.html"  # or "shop/product_list.html"
    # context_object_name = "products"
    context_object_name = "items"
    # paginate_by = 9  # optional: adds pagination

    # context = {
    #     "cart_items": request.session.get("cart", [])
    # }