# Generated by Django 5.0.2 on 2024-03-25 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_merge_20240314_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defuser',
            name='email_password',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Пароль от почтового ящика'),
        ),
        migrations.AlterField(
            model_name='defuser',
            name='position',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.position', verbose_name='Должность'),
        ),
    ]
