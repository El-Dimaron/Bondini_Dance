import random

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel


class Category(BaseModel):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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


class ItemColor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ItemSize(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size


class Item(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    colors = models.ManyToManyField(ItemColor, blank=True, related_name="items")
    sizes = models.ManyToManyField(ItemSize, blank=True, related_name="items")
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
    discount = models.SmallIntegerField(default=0)
    new_collection = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def items_count(self):
        return self.items.count()

    @property
    def is_on_sale(self):
        return self.discount > 0

    @property
    def discounted_price(self):
        return self.price - abs(self.discount)

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


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name="extra_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/items"/extra')


class Favorite(BaseModel):
    user = models.ForeignKey(get_user_model(), related_name="favorite", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="favorite", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "item")

    def __str__(self):
        return f"{self.item.name} favorited by {self.user.get_full_name}"


class Basket(BaseModel):
    user = models.ForeignKey(get_user_model(), related_name="basket", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        user_name = self.user.get_full_name if self.user else "Unknown user"
        return f"Basket №{self.id} created by {user_name}"


class BasketItem(BaseModel):
    basket = models.ForeignKey(Basket, related_name="basket_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_color = models.CharField(max_length=50, blank=True, null=True)
    selected_size = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["id"]

    @property
    def unit_price(self):
        return self.item.discounted_price if self.item.is_on_sale else self.item.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class Order(BaseModel):
    basket = models.OneToOneField(Basket, related_name="order", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(_("Повне імʼя"), max_length=150)
    phone_number = PhoneNumberField(_("Номер телефону"))
    email = models.EmailField(_("Email"), null=True, blank=True)
    notes = models.TextField(_("Примітки"), max_length=150, blank=True)
    telegram_sent = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("created", "Створений"),
            ("in_progress", "Опрацьовується"),
            ("completed", "Виконаний"),
            ("cancelled", "Скасований"),
        ],
        default="created",
    )

    def __str__(self):
        return f"Order #{self.pk} - {self.full_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.basket.basket_items.all())
