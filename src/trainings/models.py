import random

from django.contrib.auth import get_user_model
from django.db import models
from faker import Faker

from trainings.constants.choices import DAYS_OF_WEEK


class PlanNames(models.TextChoices):
    GROUP = "0", "Абонемент"
    PERSONAL = "1", "Індивідуальне тренування"


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
    schedules = models.ManyToManyField("Schedule", related_name="groups", blank=True)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def generate_groups(cls, count):
        for _ in range(count):
            group = cls.objects.create(
                name=Faker().word(),
                plan_name=random.choice((PlanNames.GROUP, PlanNames.PERSONAL)),
                description=Faker().text(max_nb_chars=100),
                price=random.choice((250, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1500, 1800, 2000)),
                trainer=Faker().name(),
            )
            users = get_user_model().objects.all()
            if users.exists():
                group.users.set(random.sample(list(users.all()), k=random.randint(5, 15)))


class Schedule(models.Model):
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=10)
    time = models.TimeField()

    @classmethod
    def generate_schedule(cls, count):
        for _ in range(count):
            cls.objects.create(
                group=random.choice(Group.objects.all()),
                day=random.choice(DAYS_OF_WEEK)[0],
                time=Faker().time(),
            )

    def __str__(self):
        return f"{self.get_day_display()} - {self.time}"
