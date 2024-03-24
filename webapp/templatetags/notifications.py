from django import template
from webapp.models import Task

register = template.Library()


@register.simple_tag
def new_task_count(user):
    return Task.objects.filter(status='1', destination_to_user=user).count()


@register.simple_tag
def notifications(user):
    return Task.objects.filter(status='1', destination_to_user=user)