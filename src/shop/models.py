import random

from django.contrib.auth import get_user_model
from django.db import models
from faker import Faker

from common.models import BaseModel


class Category(BaseModel):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def generate_categories(cls, count):
        for i in range(count):
            category = Category(name=f"{Faker().word()}")
            category.save()
        return Category.objects.all()


class Tag(BaseModel):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def generate_tags(cls, count):
        for i in range(count):
            tag = Tag(name=f"{Faker().word()}")
            tag.save()
        return Tag.objects.all()


class Item(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    part_number = models.CharField(max_length=100, unique=True)
    image = models.ImageField(default="default.png", upload_to="shop/items", null=True, blank=True)
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

    def items_count(self):
        return self.items.count()

    @classmethod
    def generate_items(cls, count):
        num = 0
        clothing_items = [
            "T-shirt",
            "Jeans",
            "Sweater",
            "Hoodie",
            "Jacket",
            "Sneakers",
            "Cap",
            "Shorts",
            "Long Shorts",
            "Leggins",
            "Skirt",
            "Scarf",
            "Gloves",
        ]
        categories = Category.objects.all()
        tags = Tag.objects.all()

        for i in range(count):
            item = cls.objects.create(
                name=f"{random.choice(clothing_items)} - {num}",
                description=Faker().text(max_nb_chars=250),
                price=random.randint(200, 3000),
                part_number=f"bd_item_{num}_{random.randint(1, 500)}",
                available=random.choice(("in_stock", "not_available", "contact_us")),
                category=random.choice(categories) if categories else None,
            )

            if tags.exists():
                item.tags.set(random.sample(list(tags.all()), k=random.randint(1, 3)))
            num += 1


class Favorite(BaseModel):
    user = models.ForeignKey(get_user_model(), related_name="favorite", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="favorite", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "item")


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
