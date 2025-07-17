from django.forms import models

from trainings.models import Group


class GroupForm(models.ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
            "plan_name",
            "description",
            "price",
            "trainer",
            "users",
        ]
