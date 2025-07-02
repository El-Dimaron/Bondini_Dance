from celery import Celery

app = Celery("bd")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
