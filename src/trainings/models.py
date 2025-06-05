from django.contrib.auth import get_user_model
from django.db import models

from trainings.constants.choices import DAYS_OF_WEEK


class PlanNames(models.TextChoices):
    GROUP = "group", "Абонемент"
    PERSONAL = "person", "Індивідуальне тренування"


class Group(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)

    plan_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        choices=PlanNames.choices,
        default=PlanNames.GROUP,
    )

    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    trainer = models.CharField(max_length=100, null=True, blank=True)

    users = models.ManyToManyField(get_user_model(), related_name="dance_groups", blank=True)

    def __str__(self):
        return f"{self.name}"


class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=10)
    time = models.TimeField()
