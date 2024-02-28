from django.contrib.auth.models import AbstractUser
from django.db import models


class DefUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя сотрудника')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия сотрудника')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество', null=True, blank=True)
    email = models.EmailField(verbose_name='Почтовый адрес')
    position = models.ForeignKey('Position', max_length=30, verbose_name='Должность', on_delete=models.CASCADE,
                                 null=True, blank=True)
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона', null=True, blank=True)


def __str__(self):
    return self.username


class Position(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название должности')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='Отдел')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название отдела')
