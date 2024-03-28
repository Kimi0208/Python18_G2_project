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
    parent_task = models.ForeignKey('Task', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Подзадача',
                                    related_name='tasks')
    destination_to_department = models.ForeignKey('accounts.Department', verbose_name='На какой отдел задача',
                                                  on_delete=models.SET_NULL, null=True, blank=True)
    destination_to_user = models.ForeignKey('accounts.DefUser', verbose_name='На какого сотрудника задача',
                                            on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='Тип')
    attachment = models.FileField(upload_to='tasks', verbose_name='Вложение', default=None, blank=True,
                                  null=True)
    history = HistoricalRecords()

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
    file = models.FileField(verbose_name="Файлы", upload_to='uploads/', null=True, blank=True)
    user = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE, verbose_name='От кого', null=True,
                             blank=True)
    history = HistoricalRecords()


class Checklist(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    users = models.ManyToManyField('accounts.DefUser', verbose_name='Сотрудники', related_name='checklists')

    def __str__(self):
        return f'{self.name}'


class InOutMailsStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')


class InOutMailsType(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип')


class InOutMails(models.Model):
    mail_number = models.CharField(auto_created=True, max_length=250, verbose_name='Порядковый номер документа',
                                   null=True, blank=True)
    registration_date = models.DateTimeField(auto_now=True, verbose_name='Дата/Время регистрации документа',
                                             null=True, blank=True)
    input_mail_number = models.CharField(max_length=250, verbose_name='Номер исходящего письма отправителя',
                                         null=True, blank=True)
    sender_name = models.CharField(max_length=250, verbose_name='Наименование отправителя', null=True, blank=True)
    mail_description = models.TextField(max_length=250, verbose_name='Тема сообщения', null=True, blank=True)
    pages_count = models.IntegerField(default=0, verbose_name='Количество страниц', null=True, blank=True)
    responsible_department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE,
                                               verbose_name='Ответственный отдел', null=True, blank=True)
    responsible_employee = models.ForeignKey('accounts.Position', on_delete=models.CASCADE,
                                             verbose_name='Ответственный сотрудник', null=True, blank=True)
    attachment = models.FileField(upload_to='mails/%InOutMails.type', null=True, blank=True)
    initiator_of_mail = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE,
                                          verbose_name='Инициатор исходящего письма')
    status = models.ForeignKey('InOutMailsStatus', on_delete=models.CASCADE, verbose_name='Статус письма')
    type = models.ForeignKey('InOutMailsType', on_delete=models.CASCADE, verbose_name='Тип письма')


class CompaniesList(models.Model):
    company_code = models.CharField(max_length=250, verbose_name='Код компании')
    company_name = models.CharField(max_length=250, verbose_name='Назыание компании')
    contract_with_company = models.FileField(upload_to='companies/%CompaniesList.company_code', null=True, blank=True)
    company_inn = models.CharField(max_length=250, verbose_name='ИНН Компании', null=True, blank=True)


class ContractLocation(models.Model):
    location_name = models.CharField(max_length=250, verbose_name='Физическое расположение договора')


class ContractRegistry(models.Model):
    company = models.ForeignKey('CompaniesList', on_delete=models.CASCADE, verbose_name='Компания', null=True,
                                blank=True)
    input_contract_number = models.CharField(max_length=250, verbose_name='Порядковый номер входяшего документа',
                                             null=True, blank=True)
    description = models.TextField(max_length=250, verbose_name='Описание документа', null=True, blank=True)
    consultion_date = models.DateField(auto_now_add=False, verbose_name='Дата заключения договора', null=True,
                                       blank=True)
    responsible_employee = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE,
                                             verbose_name='Ответственный сотрудник', null=True, blank=True)
    scan_copy = models.BooleanField(default=False, verbose_name='Наличие отсканированной копии')
    attachment = models.FileField(upload_to='contracts/%ContractRegistry.company', null=True, blank=True)
    contract_location = models.ForeignKey('ContractLocation', on_delete=models.CASCADE,
                                          verbose_name='Физическое расположение договора')
