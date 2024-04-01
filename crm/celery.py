import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
app = Celery("crm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "deadline_task_notification": {
        "task": "webapp.tasks.deadline_task_notification",
        "schedule": timedelta(seconds=30)
    }
}