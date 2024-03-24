from django import template
from webapp.models import Task
from webapp.forms import TaskForm, FileForm


register = template.Library()


@register.simple_tag
def task_form():
    new_task_form = TaskForm()
    return new_task_form
