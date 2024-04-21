from django.db import models

SCAN_CHOICES = [
        (True, 'Есть'),
        (False, 'Нет'),
    ]

class InOutMailsStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return f'{self.name}'


class OutMails(models.Model):
    out_mail_number = models.CharField(max_length=20, verbose_name='Исходящий № документа')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    receiver = models.CharField(max_length=100, verbose_name='Кому адресован документ')
    description = models.TextField(max_length='1500', null=True, blank=True, verbose_name='Краткое описание')
    pages_count = models.CharField(max_length=10, verbose_name='Количество страниц', null=True, blank=True)
    input_mail_number = models.CharField(max_length=20, verbose_name='Номер входящего документа', null=True, blank=True)
    responsible_person = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE,
                                           verbose_name='Исполнитель')
    scan = models.BooleanField(default=False, verbose_name='Наличие скан копии', choices=SCAN_CHOICES)
    status = models.ForeignKey('InOutMailsStatus', verbose_name='Статус', on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField(max_length='1500', null=True, blank=True, verbose_name='Комментарии')
    attachment = models.FileField(upload_to='uploads/out_mails/', null=True, blank=True, verbose_name='Вложение')

    def get_scan_status(self):
        if self.scan:
            return "Есть"
        else:
            return "Нет"


class InMails(models.Model):
    in_mail_number = models.CharField(max_length=20, verbose_name='Входящий № документа')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    mail_number = models.CharField(max_length=20, verbose_name='№ номер поступившего документа')
    sender = models.CharField(max_length=100, verbose_name='От кого поступило сообщение')
    description = models.TextField(max_length=1500, verbose_name='Краткое описание', null=True, blank=True)
    pages_count = models.CharField(max_length=20, verbose_name='Кол-во страниц', null=True, blank=True)
    responsible_person = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE,
                                           verbose_name='Кому передан на исполнение')
    output_mail_number = models.CharField(max_length=20, verbose_name='Номер исходящего документа', null=True,
                                          blank=True)
    scan = models.BooleanField(default=False, verbose_name='Наличие скан копии', choices=SCAN_CHOICES)
    status = models.ForeignKey('InOutMailsStatus', verbose_name='Статус', on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField(max_length=1500, verbose_name='Коментарии', null=True, blank=True)
    attachment = models.FileField(upload_to='uploads/in_mails/', null=True, blank=True, verbose_name='Вложение')

    def get_scan_status(self):
        if self.scan:
            return "Есть"
        else:
            return "Нет"


class CompaniesList(models.Model):
    company_code = models.CharField(max_length=250, verbose_name='Код компании')
    company_name = models.CharField(max_length=250, verbose_name='Название компании')
    attachment = models.FileField(upload_to='uploads/companies/', null=True, blank=True, verbose_name='Вложение')
    contract_location = models.ForeignKey('ContractLocation', on_delete=models.CASCADE,
                                          verbose_name='Физическое расположение документа', null=True, blank=True)
    company_inn = models.CharField(max_length=250, verbose_name='ИНН Компании', null=True, blank=True)

    def __str__(self):
        return f'{self.company_code} {self.company_name}'


class ContractLocation(models.Model):
    location_name = models.CharField(max_length=250, verbose_name='Физическое расположение договора')

    def __str__(self):
        return f'{self.location_name}'


class ContractRegistry(models.Model):
    document_auto_number = models.IntegerField(auto_created=True, verbose_name='', null=True, blank=True)
    company = models.ForeignKey('CompaniesList', on_delete=models.CASCADE, verbose_name='Компания', null=True,
                                blank=True)
    input_contract_number = models.CharField(max_length=250, verbose_name='Порядковый номер входяшего документа',
                                             null=True, blank=True)
    description = models.TextField(max_length=250, verbose_name='Описание документа', null=True, blank=True)
    consultion_date = models.DateField(auto_now_add=False, verbose_name='Дата заключения договора', null=True,
                                       blank=True)
    responsible_employee = models.ForeignKey('accounts.DefUser', on_delete=models.CASCADE,
                                             verbose_name='Ответственный сотрудник', null=True, blank=True)
    scan_copy = models.BooleanField(default=False, verbose_name='Наличие отсканированной копии', choices=SCAN_CHOICES)
    # attachment = models.FileField(upload_to='uploads/contracts/', null=True, blank=True, verbose_name='Вложение')
    attachments = models.ManyToManyField('Attachment', blank=True, related_name='contracts')
    contract_location = models.ForeignKey('ContractLocation', on_delete=models.CASCADE,
                                          verbose_name='Физическое расположение договора')

    def get_scan_status(self):
        if self.scan_copy:
            return "Есть"
        else:
            return "Нет"


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/contracts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name