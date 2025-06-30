from django.urls import path

from trainings.views import (CreateGroupView, DeleteGroupView, ListGroupsView,
                             ScheduleView, UpdateGroupView, groups)

app_name = "groups"

urlpatterns = [
    path("", ListGroupsView.as_view(), name="get_groups"),
    path("create", CreateGroupView.as_view(), name="create_group"),
    path("update/<str:id>/", UpdateGroupView.as_view(), name="update_group"),
    path("delete/<str:id>/", DeleteGroupView.as_view(), name="delete_group"),
    path("schedule", ScheduleView.as_view(), name="schedule"),
    path("generate/", groups, name="generate_groups"),
]
