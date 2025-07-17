from django.urls import path

from blog.views import all_blogs, create

urlpatterns = [
    path("", all_blogs),
    path("create/", create),
]
