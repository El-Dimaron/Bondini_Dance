from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from shop.models import Basket, BasketItem, Favorite, Item
from shop.tasks import (generate_categories, generate_items, generate_tags,
                        mine_bitcoin)


class ProductListView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            user_favorites = set(Favorite.objects.filter(user=self.request.user).values_list("item_id", flat=True))
            for item in qs:
                item.is_favorited = item.id in user_favorites
        else:
            for item in qs:
                item.is_favorited = False

        return qs


class ProductDetailsView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "item"


class FavoriteView(ListView):
    model = Item
    template_name = "favorite.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(favorite__user=self.request.user)


@method_decorator(login_required, name="dispatch")
class ToggleFavoriteView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

        if not created:
            favorite.delete()

        return redirect(request.META.get("HTTP_REFERER", "index"))


class BasketView(ListView):
    model = Basket
    template_name = "basket.html"
    context_object_name = "items"

    def get_queryset(self):
        return BasketItem.objects.filter(basket__user=self.request.user, basket__is_submitted=False).select_related(
            "item"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            basket_items = BasketItem.objects.filter(basket__user=self.request.user, basket__is_submitted=False)
            total = 0
            for basket_item in basket_items:
                total += basket_item.quantity * basket_item.item.price

            context["total"] = total

        return context


class BasketUpdateView(View):
    def post(self, request, item_id):
        action = request.POST.get("action")
        basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user, basket__is_submitted=False)

        if action == "increase":
            basket_item.quantity += 1
            basket_item.save()

        if action == "decrease":
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket_item.delete()

        if action == "delete":
            basket_item.delete()

        return redirect(request.META.get("HTTP_REFERER", "basket"))


@method_decorator(login_required, name="dispatch")
class AddToBasketView(View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)

        basket, _ = Basket.objects.get_or_create(user=request.user, is_submitted=False)

        basket_item, created = BasketItem.objects.get_or_create(basket=basket, item=item)

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return redirect(request.META.get("HTTP_REFERER", "index"))


def bitcoin(request: HttpRequest) -> HttpResponse:
    mine_bitcoin.delay()
    return HttpResponse("Task started")


def items(request: HttpRequest) -> HttpResponse:
    try:
        count = int(request.GET.get("count", 1))
    except ValueError:
        count = 1
    generate_items.delay(count)
    return HttpResponse("Task generate_items started")


def tags(request: HttpRequest) -> HttpResponse:
    try:
        count = int(request.GET.get("count", 1))
    except ValueError:
        count = 1
    generate_tags.delay(count)
    return HttpResponse("Task generate_tags started")


def categories(request: HttpRequest) -> HttpResponse:
    try:
        count = int(request.GET.get("count", 1))
    except ValueError:
        count = 1
    generate_categories.delay(count)
    return HttpResponse("Task generate_categories started")
