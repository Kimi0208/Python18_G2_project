from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords


class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок задачи')
    description = models.TextField(max_length=2500, verbose_name='Описание задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания задачи')
    start_date = models.DateTimeField(verbose_name='Приступить к задаче', null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления задачи')
    done_at = models.DateTimeField(verbose_name='Время завершения задачи', null=True, blank=True)
    deadline = models.DateTimeField(null=True, verbose_name='Дедлайн задачи', blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус задачи', default=1)
    priority = models.ForeignKey('Priority', on_delete=models.CASCADE, verbose_name='Приоритет задачи')
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор задачи',
                               related_name='task_author', null=True)
    parent_task = models.ForeignKey('Task', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name='Связанная задача', related_name='tasks')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел задача',
                                                  on_delete=models.SET_NULL, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.DefUser', verbose_name='На какого сотрудника задача',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='Тип')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}){self.title}'


class Type(models.Model):
    name = models.CharField(max_length=25, verbose_name='Тип')

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор комментария')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Комментарий к задаче', related_name='comments',
                             null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.description}'


class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name='Статус задачи/заявки')

    def __str__(self):
        return f'{self.name}'


class Priority(models.Model):
    name = models.CharField(max_length=10, verbose_name='Приоритет задачи/заявки')

    def __str__(self):
        return f'{self.name}'


class File(models.Model):
    file = models.FileField(verbose_name="Файлы", upload_to='uploads/user_docs', null=True, blank=True)
    user = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='От кого', null=True,
                             blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Задача', null=True, blank=True)
    checklist = models.ForeignKey('Checklist', on_delete=models.CASCADE, verbose_name='Чеклист', null=True,
                                  blank=True, related_name='files')
    history = HistoricalRecords()


class FileSignature(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='Файл')
    user = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Задача')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Checklist(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    users = models.ManyToManyField('accounts.DefUser', verbose_name='Сотрудники', related_name='checklists')

    def __str__(self):
        return f'{self.name}'