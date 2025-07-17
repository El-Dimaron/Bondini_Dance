from django.urls import include, path
from rest_framework import routers

from api.views import (GroupCreateApiView, GroupListApiView,
                       GroupRetreiveUpdateDeleteApiView, UserViewSet)

app_name = "api"
user_router = routers.DefaultRouter()
user_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(user_router.urls)),
    path("groups/", GroupListApiView.as_view(), name="group_list"),
    path("groups/create", GroupCreateApiView.as_view(), name="group_create"),
    path("groups/<pk>/", GroupRetreiveUpdateDeleteApiView.as_view(), name="group_retreive"),
]
