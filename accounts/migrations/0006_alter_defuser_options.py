# Generated by Django 5.0.2 on 2024-05-12 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_defuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defuser',
            options={'permissions': [('chief_department_edit_tasks', 'Могут редактировать все задачи своего отдела')]},
        ),
    ]