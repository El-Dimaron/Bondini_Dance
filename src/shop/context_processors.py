from django.db import models

from .models import BasketItem


def basket_quantity(request):
    if request.user.is_authenticated:
        quantity = (
            BasketItem.objects.filter(basket__user=request.user, basket__is_submitted=False).aggregate(
                total=models.Sum("quantity")
            )["total"]
            or 0
        )
    else:
        quantity = 0

    return {"basket_quantity": quantity}
