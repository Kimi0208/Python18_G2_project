# Generated by Django 5.0.2 on 2024-02-20 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.department', verbose_name='Отдел'),
        ),
    ]
