from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date', 'deadline',
                  'status', 'parent_task', 'destination_to_department', 'destination_to_user']
