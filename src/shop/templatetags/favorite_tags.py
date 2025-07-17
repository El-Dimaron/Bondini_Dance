from django import template

from shop.models import Favorite

register = template.Library()


@register.filter
def is_favorited_by(item, user):
    if not user.is_authenticated:
        return False
    return Favorite.objects.filter(user=user, item=item).exists()
