from django.urls import path

from shop.views import (AddToBasketView, BasketUpdateView, BasketView,
                        FavoriteView, ProductDetailsView, ProductListView,
                        ToggleFavoriteView, bitcoin, categories, items, tags)

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("favourite/", FavoriteView.as_view(), name="favorites"),
    path("item/<int:item_id>/favorite/", ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("basket/", BasketView.as_view(), name="basket"),
    path("basket/update/<int:item_id>/", BasketUpdateView.as_view(), name="basket_update"),
    path("item/<int:item_id>/basket/", AddToBasketView.as_view(), name="add_to_basket"),
    path("bitcoin", bitcoin, name="bitcoin"),
    path("generate-items", items, name="generate_items"),
    path("generate-tags", tags, name="generate_tags"),
    path("generate-categories", categories, name="generate_categories"),
]
