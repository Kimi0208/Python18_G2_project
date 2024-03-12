import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
app = Celery("crm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "deadline_task_notification": {
        "task": "webapp.tasks.deadline_task_notification",
        "schedule": 30.0
    }
}