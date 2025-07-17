import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from shop.forms import OrderForm
from shop.models import (Basket, BasketItem, Category, Favorite, Item, Order,
                         Tag)
from shop.utils.email import new_order_email


class ProductListView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        query = request.GET.get("search")
        categories = request.GET.getlist("category")
        statuses = request.GET.getlist("status")
        sort_option = request.GET.get("sort")

        if query:
            search_fields = ["name", "part_number"]
            self.request.session[f"search_fields_{datetime.datetime.now()}"] = query
            or_filter = Q()
            for field in search_fields:
                or_filter |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(or_filter)

        if categories:
            queryset = queryset.filter(category__slug__in=categories)

        if statuses:
            queryset = queryset.filter(available__in=statuses)

        queryset = queryset.annotate(
            in_stock_priority=Case(
                When(Q(available__in=["in_stock", "contact_us"]), then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )

        if sort_option == "price_asc":
            queryset = queryset.order_by("in_stock_priority", "price")
        elif sort_option == "price_desc":
            queryset = queryset.order_by("in_stock_priority", "-price")
        else:
            queryset = queryset.order_by("in_stock_priority", "name")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_query"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["categories"] = Category.objects.all()
        context["selected_status"] = self.request.GET.get("status", "")
        context["availability_statuses"] = dict(Item._meta.get_field("available").choices)
        context["selected_sort"] = self.request.GET.get("sort", "")
        context["selected_categories"] = self.request.GET.getlist("category")
        context["selected_statuses"] = self.request.GET.getlist("status")

        category_label = ""
        if category := self.request.GET.get("category"):
            category_obj = Category.objects.filter(slug=category).first()
            if category_obj:
                category_label = category_obj.name
        context["category_label"] = category_label

        status_label = ""
        statuses = dict(Item._meta.get_field("available").choices)
        if status_key := self.request.GET.get("status"):
            status_label = statuses.get(status_key, "")
        context["status_label"] = status_label

        return context


class ProductDetailsView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "item"


class SaleView(ListView):
    model = Item
    template_name = "sale.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(discount__gt=0)


class NewCollectionView(ListView):
    model = Item
    template_name = "new_collection.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(new_collection=True)


class FavoriteView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "favorite.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(favorite__user=self.request.user).order_by("-favorite__updated_at")


@method_decorator(login_required, name="dispatch")
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)

        if not created:
            favorite.delete()

        return redirect(request.META.get("HTTP_REFERER", "index"))


class BasketView(LoginRequiredMixin, ListView):
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
                total += basket_item.quantity * basket_item.unit_price

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
        color = request.POST.get("selected_color")
        size = request.POST.get("selected_size")

        basket, _ = Basket.objects.get_or_create(user=request.user, is_submitted=False)

        basket_item, created = BasketItem.objects.get_or_create(
            basket=basket, item=item, selected_color=color, selected_size=size
        )

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        messages.success(
            request,
            mark_safe(
                f"«{item.name}» додано до кошика. "
                f"<a href='{reverse('shop:basket')}'"
                f"class='text-white text-decoration-underline fw-semibold'>Перейти</a>"
            ),
        )

        return redirect(request.META.get("HTTP_REFERER", "index"))


class OrderCompleteView(View):
    model = Basket
    template_name = "order.html"
    context_object_name = "cart"

    def get(self, request):
        return render(request, "order_form.html")

    def get_queryset(self):
        return BasketItem.objects.filter(basket__user=self.request.user, basket__is_submitted=False).select_related(
            "item"
        )


class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "order_form.html"
    form_class = OrderForm
    success_url = reverse_lazy("shop:order_success")

    def get_basket(self):
        return Basket.objects.filter(user=self.request.user, is_submitted=False).first()

    def dispatch(self, request, *args, **kwargs):
        if not self.get_basket():
            return redirect("shop:basket")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        if user.first_name or user.last_name:
            initial["full_name"] = f"{user.first_name} {user.last_name}".strip()

        if hasattr(user, "phone_number") and user.phone_number:
            initial["phone_number"] = user.phone_number

        if user.email:
            initial["email"] = user.email

        return initial

    def form_valid(self, form):
        basket = self.get_basket()
        order = form.save(commit=False)
        order.user = self.request.user
        order.basket = basket
        order.save()

        basket.is_submitted = True
        basket.save()

        self.request.session["order_id"] = order.id

        new_order_email(order, self.request)

        return redirect("shop:order_success")


class OrderSuccessView(TemplateView):
    template_name = "order_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.pop("order_id", None)

        if not order_id:
            return redirect("shop:home")

        context["order"] = get_object_or_404(Order, id=order_id)
        return context


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "order_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        qs = Order.objects.select_related("user", "basket")
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs.order_by("-submitted_at")


def items(request: HttpRequest) -> HttpResponse:
    if request.user.has_perm("shop.add_item"):
        word = ""
        try:
            count = int(request.GET.get("count", 1))
        except ValueError:
            count = 1
        Item.generate_items(count)
        if count > 1:
            word = "ies"
        return HttpResponse(f"Generated {count} item{word}")
    else:
        return HttpResponseForbidden("You don't have permission.")


def tags(request: HttpRequest) -> HttpResponse:
    if request.user.has_perm("shop.add_tag"):
        word = ""
        try:
            count = int(request.GET.get("count", 1))
        except ValueError:
            count = 1
        Tag.generate_tags(count)
        if count > 1:
            word = "s"
        return HttpResponse(f"Generated {count} tag{word}")
    else:
        return HttpResponseForbidden("You don't have permission.")


def categories(request: HttpRequest) -> HttpResponse:
    if request.user.has_perm("shop.add_category"):
        word = "y"
        try:
            count = int(request.GET.get("count", 1))
        except ValueError:
            count = 1
        Category.generate_categories(count)
        if count > 1:
            word = "ies"
        return HttpResponse(f"Generated {count} categor{word}")
    else:
        return HttpResponseForbidden("You don't have permission.")


def test_tag_view(request):
    return render(request, "test.html")
