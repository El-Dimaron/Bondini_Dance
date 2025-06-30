from django.urls import path

from shop.views import (ProductDetailsView, ProductListView, bitcoin,
                        categories, items, tags)

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("bitcoin", bitcoin, name="bitcoin"),
    path("generate-items", items, name="generate_items"),
    path("generate-tags", tags, name="generate_tags"),
    path("generate-categories", categories, name="generate_categories"),
]
