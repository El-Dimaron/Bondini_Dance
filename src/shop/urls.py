from django.urls import path

from shop.views import ProductListView

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
]
