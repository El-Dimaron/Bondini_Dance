from celery import shared_task

from accounts.models import User


@shared_task
def generate_users(count=1):
    User.generate_users(count)
