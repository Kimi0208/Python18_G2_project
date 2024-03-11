# Generated by Django 5.0.2 on 2024-03-03 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_defuser_email_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defuser',
            name='email_password',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Пароль почты'),
        ),
        migrations.AlterField(
            model_name='defuser',
            name='position',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.position', verbose_name='Должность'),
        ),
    ]
