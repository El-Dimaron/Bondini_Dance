import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView, TemplateView,
                                  UpdateView, View)
from webargs import fields
from webargs.djangoparser import use_args

from trainings.constants.choices import DAYS_OF_WEEK
from trainings.forms import GroupForm
from trainings.models import Group


class ListGroupsView(ListView):
    model = Group
    template_name = "groups/groups.html"
    context_object_name = "groups"

    query_args = {
        "name": fields.Str(required=False),
        "trainer": fields.Str(required=False),
    }

    @use_args(query_args, location="query")
    def get_queryset(self, args):
        queryset = super().get_queryset()

        query = self.request.GET.get("search", None)

        if query:
            search_fields = ["name", "trainer"]
            self.request.session[f"search_fields_{datetime.datetime.now()}"] = query
            or_filter = Q()
            for field in search_fields:
                or_filter |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(or_filter)

        return queryset


class CreateGroupView(CreateView):
    model = Group
    template_name = "groups/create.html"
    form_class = GroupForm
    success_url = reverse_lazy("groups:get_groups")


class UpdateGroupView(UpdateView):
    model = Group
    template_name = "groups/update.html"
    form_class = GroupForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("groups:get_groups")


class DeleteGroupView(View):
    def get(self, request, id, *args, **kwargs):
        group = get_object_or_404(Group, id=id)
        group.delete()
        return redirect(reverse_lazy("groups:get_groups"))


class ScheduleView(TemplateView):
    template_name = "groups/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        days = [day[0] for day in DAYS_OF_WEEK]
        keys = [day[1] for day in DAYS_OF_WEEK]

        groups = Group.objects.prefetch_related("schedules").all()
        calendar_data = []

        for group in groups:
            row = {"name": group.name, "schedule": {day: "" for day in days}}
            for schedule in group.schedules.all():
                if schedule.day in row["schedule"]:
                    row["schedule"][schedule.day] = schedule.time.strftime("%H:%M")
            calendar_data.append(row)

        context["days"] = days
        context["day_keys"] = keys
        context["calendar_data"] = calendar_data
        return context
