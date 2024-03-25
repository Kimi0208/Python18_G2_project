from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from crm import settings


class DefUser(AbstractUser):

    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Имя сотрудника')
    last_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Фамилия сотрудника')

    email = models.EmailField(null=False, blank=False, verbose_name='Почтовый адрес')
    email_password = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Пароль от почтового ящика')
    position = models.ForeignKey('Position', max_length=30, verbose_name='Должность', on_delete=models.CASCADE,

                                 null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=False, blank=False, verbose_name='Номер телефона')
    signature = models.FileField(verbose_name="Подпись", upload_to='uploads/signature', null=True, blank=True)

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        if self.email_password and type(self.email_password) != bytes:
            cipher_suite = Fernet(settings.SECRET_KEY)
            try:
                self.email_password = cipher_suite.encrypt(self.email_password.encode('utf-8'))
                self.email_password = self.email_password.decode('utf-8')
            except InvalidToken:
                pass
        super().save(*args, **kwargs)

    def decrypt_email_password(self):
        if self.email_password:
            cipher_suite = Fernet(settings.SECRET_KEY)
            try:
                decrypted_password = cipher_suite.decrypt(self.email_password).decode('utf-8')
                return decrypted_password
            except InvalidToken:
                return 'Invalid key'
        return 'No password provided'


class Position(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название должности', unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='Отдел')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название отдела', unique=True)

    def __str__(self):
        return self.name
