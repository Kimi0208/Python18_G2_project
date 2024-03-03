from django.db import models


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'Новая'),
        ('Accepted', 'Принятая'),
        ('Not accepted', 'Не принятая'),
        ('At work', 'В работе'),
        ('Suspended', 'Приостановлена'),
    )
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(max_length=2500, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    start_date = models.DateTimeField(verbose_name='Начало', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    done_at = models.DateTimeField(auto_now=True, verbose_name='Завершенно')
    deadline = models.DateField(null=True, verbose_name='Дедлайн')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Статус', default='Новая')
    priority = models.ForeignKey('webapp.Priority', on_delete=models.CASCADE, verbose_name='Приоритет', null=True,
                                 blank=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='Автор',
                               related_name='task_author')
    parent_task = models.ForeignKey('webapp.Task', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name='Подзадача', related_name='tasks')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел задача',
                                                  on_delete=models.CASCADE, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.CustomUser', verbose_name='На какого сотрудника задача',
                                            on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.author}'


class Proposal(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(max_length=2500, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    start_date = models.DateTimeField(verbose_name='Приступить к заявке', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления заявки')
    done_at = models.DateTimeField(auto_now=True, verbose_name='Время завершения заявки')
    deadline = models.DateField(null=True, verbose_name='Дедлайн заявки')
    status = models.ForeignKey('webapp.Status', on_delete=models.CASCADE, verbose_name='Статус заявки', null=True,
                               blank=True)
    priority = models.ForeignKey('webapp.Priority', on_delete=models.CASCADE, verbose_name='Приоритет заявки',
                                 null=True,
                                 blank=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='Автор задачи',
                               related_name='proposal_author')
    parent_task = models.ForeignKey('webapp.Task', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name='Подзадача/задача')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел заявка',
                                                  on_delete=models.CASCADE, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.CustomUser', verbose_name='На какого сотрудника заявка',
                                            on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='Автор')
    task = models.ForeignKey('webapp.Task', on_delete=models.CASCADE, verbose_name='Коммент к задаче',
                             related_name='comments',
                             null=True, blank=True)
    proposal = models.ForeignKey('webapp.Proposal', on_delete=models.CASCADE, verbose_name='Коммент к заявке',
                                 related_name='comments', null=True, blank=True)
    text_comment = models.TextField(max_length=2500, verbose_name='Текст комментария')

    def __str__(self):
        return self.text_comment


class Status(models.Model):
    name = models.CharField(max_length=10, verbose_name='Статус заявки')

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=10, verbose_name='Приоритет задачи/заявки')

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(verbose_name="Файлы", upload_to='user_docs/', null=True, blank=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='От кого', default=1)
    task = models.ForeignKey('webapp.Task', on_delete=models.CASCADE, verbose_name='Задача', default=1)
