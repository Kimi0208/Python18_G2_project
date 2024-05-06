from datetime import datetime
from celery import shared_task
from webapp.models import Task
from webapp.views.mail_send import send_email_notification


@shared_task()
def deadline_task_notification():
    tasks = Task.objects.exclude(status__name='Выполнена').filter(deadline__lt=datetime.now())
    for task in tasks:
        if task.destination_to_user:
            subject = f'CRM: Задача #{task.id} истек дедлайн {task.title}'
            message = f'Дата дедлайна: {task.deadline}'
            try:
                send_email_notification(subject, message, task.author.email)
            except Exception as e:
                print(f"Ошибка при отправке электронного уведомления: {e}")