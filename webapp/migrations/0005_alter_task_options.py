# Generated by Django 5.0.2 on 2024-05-12 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': [('chief_department_edit_tasks', 'Могут редактировать все задачи своего отдела'), ('ordinary_employee_edit_tasks', 'Могут редактировать только свои задачи')]},
        ),
    ]
