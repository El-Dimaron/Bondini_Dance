from django.conf import settings
from django.core.mail import send_mail


def new_order_email(order, request):
    subject = f"Нове замовлення №{order.id}"

    items_text = ""
    for item in order.basket.basket_items.all():
        items_text += (
            f"• {item.item.name}\n"
            f"  Колір: {item.selected_color if item.selected_color else '-'}\n"
            f"  Розмір: {item.selected_size if item.selected_size else '-'}\n"
            f"  Ціна: {item.item.price} грн\n"
            f"  Кількість: {item.quantity}\n"
        )

    body = (
        f"Створено замовлення: {order.id}\n"
        f"Дата: {order.submitted_at.strftime('%d.%m.%Y')}\n"
        f"Ім’я: {order.full_name}\n"
        f"Телефон: {order.phone_number}\n"
        f"Email: {order.email or '-'}\n"
        f"Примітки: {order.notes or '-'}\n\n"
        f"Замовлені товари:\n"
        f"{items_text}"
        f"Сума до оплати: {order.total_price} грн\n"
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )
