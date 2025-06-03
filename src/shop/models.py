from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name


class Item(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    part_number = models.CharField(max_length=100, unique=True)
    image = models.ImageField(default="default.png", upload_to="media/shop/items", null=True, blank=True)
    available = models.CharField(
        choices=[
            ("in_stock", "Є в наявності"),
            ("not_available", "Немає в наявності"),
            ("contact_us", "Уточніть наявність"),
        ]
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField("shop.Tag", blank=True)

    def __str__(self):
        return self.name


class Favorite(BaseModel):
    user = models.ForeignKey(get_user_model(), related_name="favorite", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="favorite", on_delete=models.CASCADE)


class Basket(BaseModel):
    user = models.ForeignKey(get_user_model(), related_name="basket", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)


class BasketItem(BaseModel):
    basket = models.ForeignKey(Basket, related_name="basket_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class OrderRequest(BaseModel):
    basket = models.OneToOneField(Basket, related_name="order_request", on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), related_name="order_request", on_delete=models.SET_NULL, null=True, blank=True
    )
    telegram_sent = models.BooleanField(default=False)
