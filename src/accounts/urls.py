from django.urls import path

from accounts.views import (ProfileEditView, ProfileView, UserActivationView,
                            users)

app_name = "accounts"

urlpatterns = [
    path("generate/", users, name="generate_users"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("profile/edit/<int:id>/", ProfileEditView.as_view(), name="edit_profile"),
    path("activate/<str:uid>/<str:token>/", UserActivationView.as_view(), name="activate_user"),
]
