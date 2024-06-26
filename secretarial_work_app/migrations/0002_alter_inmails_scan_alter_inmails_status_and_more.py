# Generated by Django 5.0.2 on 2024-04-20 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretarial_work_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmails',
            name='scan',
            field=models.CharField(max_length=10, verbose_name='Наличие скана копии'),
        ),
        migrations.AlterField(
            model_name='inmails',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='secretarial_work_app.inoutmailsstatus', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='outmails',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='secretarial_work_app.inoutmailsstatus', verbose_name='Статус'),
        ),
    ]
