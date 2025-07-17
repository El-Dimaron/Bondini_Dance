from django.contrib import admin

from accounts.models import User
from shop.models import (Basket, BasketItem, Category, Favorite, Item,
                         ItemColor, ItemImage, ItemSize, Order, Tag)
from trainings.models import Group as TrainingGroup
from trainings.models import Schedule

admin.site.register([User, Favorite, Category, Tag, Basket, Order])


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1


class ItemColorInline(admin.TabularInline):
    model = ItemColor
    extra = 1


class ItemSizeInline(admin.TabularInline):
    model = ItemSize
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "available")
    search_fields = ("name",)
    filter_horizontal = ("colors", "sizes")
    inlines = [ItemImageInline]


admin.site.register(Item, ItemAdmin)


class BasketItemAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity", "selected_color", "selected_size", "basket")
    search_fields = ("item__name", "selected_color", "selected_size")


admin.site.register(BasketItem, BasketItemAdmin)


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    min_num = 0
    max_num = 7
    fields = ("day", "time")
    ordering = ("day",)


@admin.register(TrainingGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "plan_name_display", "price", "trainer", "user_count", "schedule_count")
    list_filter = ("plan_name",)
    search_fields = ("name", "trainer", "description")
    filter_horizontal = ("users", "schedules")
    readonly_fields = ("user_count", "schedule_count")

    def plan_name_display(self, obj):
        return obj.get_plan_name_display()

    plan_name_display.short_description = "Тип абонементу"

    def user_count(self, obj):
        return obj.users.count()

    user_count.short_description = "Кількість учасників"

    def schedule_count(self, obj):
        return obj.schedules.count()

    schedule_count.short_description = "К-сть тренувань на тиждень"


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("day", "time")
    list_filter = ("day",)
    search_fields = (
        "day",
        "time",
    )
