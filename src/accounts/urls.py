from django.urls import path

from accounts.views import users

app_name = "accounts"

urlpatterns = [
    path("generate/", users, name="generate_users"),
]
