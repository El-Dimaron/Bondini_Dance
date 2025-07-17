from django import template

from shop.models import Category

register = template.Library()


@register.filter
def get_category_name(categories, slug):
    try:
        return categories.get(slug=slug).name
    except Category.DoesNotExist:
        return slug
