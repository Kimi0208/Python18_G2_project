from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class DefUser(AbstractUser):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя сотрудника')
    last_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия сотрудника')

    email = models.EmailField(null=False, blank=False, verbose_name='Почтовый адрес')
    email_password = models.CharField(max_length=500, null=True, blank=True, verbose_name='Пароль от почтового ящика')
    position = models.ForeignKey('Position', max_length=30, verbose_name='Должность', on_delete=models.CASCADE,
                                 null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер телефона')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.email_password:
            self.email_password = make_password(self.email_password)
        super().save(*args, **kwargs)


class Position(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название должности', unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='Отдел')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название отдела', unique=True)

    def __str__(self):
        return self.name
