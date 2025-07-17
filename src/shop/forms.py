from django.forms import ModelForm, Textarea

from shop.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone_number", "email", "notes"]
        widgets = {
            "notes": Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone_number"].initial = "+380"
        self.fields["phone_number"].widget.attrs["placeholder"] = "+380"
        self.fields["phone_number"].error_messages.update(
            {"invalid": "Будь ласка, введіть коректний номер телефону у форматі +380XXXXXXXXX"}
        )
