from django.urls import path

from shop.views import ProductDetailsView, ProductListView

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
]
