from django.urls import include, path
from rest_framework import routers

from api.views import GroupViewSet, UserViewSet

app_name = "api"
user_router = routers.DefaultRouter()
user_router.register("users", UserViewSet)
user_router.register("groups", GroupViewSet)

urlpatterns = [
    path("", include(user_router.urls)),
    # path("groups/<int:pk>", GroupViewSet.as_view(), name=""),
]
