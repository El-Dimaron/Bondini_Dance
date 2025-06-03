from django.contrib import admin  # NOQA: F401

from accounts.models import User
from shop.models import (Basket, BasketItem, Category, Favorite, Item,
                         OrderRequest, Tag)
from trainings.models import Group, Schedule

admin.site.register([User, Group, Schedule, Item, Favorite, Category, Tag, Basket, BasketItem, OrderRequest])
