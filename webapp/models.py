from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок задачи')
    description = models.TextField(max_length=2500, verbose_name='Описание задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания задачи')
    start_date = models.DateTimeField(verbose_name='Приступить к задаче', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления задачи')
    done_at = models.DateTimeField(auto_now=True, verbose_name='Время завершения задачи')
    deadline = models.DateField(null=True, verbose_name='Дедлайн задачи')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус задачи', null=True, blank=True)
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
    files = models.ForeignKey('File', verbose_name='Файлы')


class Proposal(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок заявки')
    description = models.TextField(max_length=2500, verbose_name='Описание заявки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания заявки')
    start_date = models.DateTimeField(verbose_name='Приступить к заявке', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления заявки')
    done_at = models.DateTimeField(auto_now=True, verbose_name='Время завершения заявки')
    deadline = models.DateField(null=True, verbose_name='Дедлайн заявки')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Статус заявки', null=True, blank=True)
    priority = models.ForeignKey('Priority', on_delete=models.CASCADE, verbose_name='Приоритет заявки', null=True,
                                 blank=True)
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор задачи',
                               related_name='proposal_author')
    parent_task = models.ForeignKey('Task', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name='Подзадача/задача')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел заявка',
                                                  on_delete=models.CASCADE, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.DefUser', verbose_name='На какого сотрудника заявка',
                                            on_delete=models.CASCADE, null=True, blank=True)
    files = models.ForeignKey('File', verbose_name='Файлы')


class Comment(models.Model):
    author = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='Автор комментария')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Коммент к задаче', related_name='comments',
                             null=True, blank=True)
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, verbose_name='Коммент к заявке',
                                 related_name='comments', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='Текст комментария')


class Status(models.Model):
    # task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Статус задачи', related_name='statuses')
    # proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, verbose_name='Статус заявки',
    #                              related_name='statuses')
    name = models.CharField(max_length=10, verbose_name='Статус задачи/заявки')


class Priority(models.Model):
    # task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Приоритет задачи',
    #                          related_name='priorities')
    # proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, verbose_name='Приоритет заявки',
    #                              related_name='priorities')
    name = models.CharField(max_length=10, verbose_name='Приоритет задачи/заявки')


class File(models.Model):
    file = models.FileField(verbose_name="Файлы", upload_to='Files/')
