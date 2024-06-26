# Generated by Django 5.0.2 on 2024-05-04 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretarial_work_app', '0007_remove_contractregistry_scan_copy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractregistry',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secretarial_work_app.companieslist', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='contractregistry',
            name='input_contract_number',
            field=models.CharField(max_length=250, verbose_name='Порядковый номер входяшего документа'),
        ),
    ]
