from django import template
from webapp.models import Task

register = template.Library()


@register.simple_tag
def new_task_count(user):
    if not user.is_authenticated:
        return 0
    return Task.objects.filter(status='1', destination_to_user=user).count()


@register.simple_tag
def notifications(user):
    if not user.is_authenticated:
        return []
    return Task.objects.filter(status='1', destination_to_user=user)