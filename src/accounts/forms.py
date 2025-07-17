from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["photo", "email", "username", "first_name", "last_name", "birth_date", "phone_number"]
        labels = {
            "photo": "Фото профілю",
            "username": "Юзернейм",
            "first_name": "Ім’я",
            "last_name": "Прізвище",
            "birth_date": "Дата народження",
            "phone_number": "Телефон",
        }
        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "placeholder": "Оберіть дату",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone_number"].error_messages.update(
            {"invalid": "Будь ласка, введіть коректний номер телефону у форматі +380XXXXXXXXX"}
        )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "phone_number", "password1", "password2"]
