from django.contrib.auth import get_user_model
from django.db import models

status_choices = [("new", "Новая"), ("accepted", "Принята"), ("no_accepted", "Не принята"), ("in_progress", "В процессе"), ("pause", "Приостановлена")]
priority_choices = [("high", "Высокий"), ("medium", "Средний"), ("low", "Низкий")]


class Task(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    author = models.ForeignKey(get_user_model(), related_name='tasks', on_delete=models.CASCADE, verbose_name='Автор задачи')
    priority = models.CharField(max_length=20, choices=priority_choices, verbose_name="Приоритет задачи")
    status = models.CharField(max_length=20, default='new', verbose_name='Статус задачи', choices=status_choices)
    deadline = models.DateTimeField(verbose_name='Дедлайн задачи')
    department = models.ForeignKey("Department", on_delete=models.CASCADE, verbose_name='Отдел')
    file = models.FileField(upload_to="", verbose_name="Файл")
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания задачи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования задачи')


class Application(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, verbose_name='Задача')
    title = models.CharField(max_length=150, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    author = models.ForeignKey(get_user_model(), related_name='applications', on_delete=models.CASCADE,
                               verbose_name='Автор заявки')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заявки')
    head_department = models.ForeignKey(get_user_model(), verbose_name='Руководитель отдела')


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE,
                               verbose_name='Автор комментария')
    comment_text = models.TextField(verbose_name="Комментарий")
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Комментарий к задаче')
    application = models.ForeignKey("Application", on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Комментарий к заявке')









