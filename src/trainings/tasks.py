from celery import shared_task

from trainings.models import Group


@shared_task
def generate_groups(count=1):
    Group.generate_groups(count)
