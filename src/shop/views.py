from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, ListView

from shop.models import Item
from shop.tasks import (generate_categories, generate_items, generate_tags,
                        mine_bitcoin)


class ProductListView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"


class ProductDetailsView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "item"


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
