from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password1", "password2"]
