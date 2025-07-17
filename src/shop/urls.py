from django.urls import path

from shop.views import (AddToBasketView, BasketUpdateView, BasketView,
                        FavoriteView, NewCollectionView, OrderCreateView,
                        OrderListView, OrderSuccessView, ProductDetailsView,
                        ProductListView, SaleView, ToggleFavoriteView,
                        categories, items, tags, test_tag_view)

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("favourite/", FavoriteView.as_view(), name="favorites"),
    path("sale/", SaleView.as_view(), name="sale"),
    path("new_collection/", NewCollectionView.as_view(), name="new_collection"),
    path("item/<int:item_id>/favorite/", ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("basket/", BasketView.as_view(), name="basket"),
    path("basket/update/<int:item_id>/", BasketUpdateView.as_view(), name="basket_update"),
    path("item/<int:item_id>/basket/", AddToBasketView.as_view(), name="add_to_basket"),
    # path("bitcoin", bitcoin, name="bitcoin"),
    path("generate-items", items, name="generate_items"),
    path("generate-tags", tags, name="generate_tags"),
    path("generate-categories", categories, name="generate_categories"),
    path("order/", OrderCreateView.as_view(), name="order"),
    path("order/success/", OrderSuccessView.as_view(), name="order_success"),
    path("order/list/", OrderListView.as_view(), name="order_list"),
    path("test", test_tag_view),
]
