from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    position = models.ForeignKey('accounts.Position', on_delete=models.CASCADE, verbose_name='Должность', blank=True,
                                 null=True)
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Отдел')
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)

    def __str__(self):
        return f'{self.username} {self.email}, {self.position}'


class Position(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название должности')
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, verbose_name='Отдел')


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название отдела')
