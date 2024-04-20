from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from crm import settings


class DefUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя сотрудника')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия сотрудника')

    email = models.EmailField(verbose_name='Почтовый адрес')
    position = models.ForeignKey('Position', max_length=30, verbose_name='Должность', on_delete=models.DO_NOTHING,
                                 null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер телефона')
    signature = models.FileField(verbose_name="Подпись", upload_to='uploads/signature', null=True, blank=True)
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')

    def __str__(self):
        if self.patronymic and self.first_name:
            return f'{self.last_name.capitalize()} {self.first_name[0].capitalize()}. {self.patronymic[0]}.'
        elif self.first_name:
            return f'{self.last_name.capitalize()} {self.first_name[0].capitalize()}.'
        else:
            return f'{self.username}'


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Должность')
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, verbose_name='Отдел')

    def __str__(self):
        return f'{self.name} ({self.department.name})'


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Отдел', unique=True)

    def __str__(self):
        return self.name
