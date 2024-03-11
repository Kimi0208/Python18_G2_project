from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок задачи')
    description = models.TextField(max_length=2500, verbose_name='Описание задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания задачи')
    start_date = models.DateTimeField(verbose_name='Приступить к задаче', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления задачи')
    done_at = models.DateTimeField(verbose_name='Время завершения задачи', null=True, blank=True)
    deadline = models.DateTimeField(null=True, verbose_name='Дедлайн задачи', blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус задачи', null=True,
                               blank=True, default=1)
    priority = models.ForeignKey('Priority', on_delete=models.CASCADE, verbose_name='Приоритет задачи', null=True,
                                 blank=True)
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор задачи',
                               related_name='task_author')
    parent_task = models.ForeignKey('Task', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Подзадача',
                                    related_name='tasks')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел задача',
                                                  on_delete=models.CASCADE, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.DefUser', verbose_name='На какого сотрудника задача',
                                            on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='Тип', null=True, blank=True)

    def __str__(self):
        return f'{self.id}){self.title}'


class Type(models.Model):
    name = models.CharField(max_length=25, verbose_name='Тип')

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор комментария')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Коммент к задаче', related_name='comments',
                             null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='Текст комментария')

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


class Checklist(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    users = models.ManyToManyField('accounts.DefUser', verbose_name='Сотрудники', related_name='checklists')

    def __str__(self):
        return f'{self.name}'