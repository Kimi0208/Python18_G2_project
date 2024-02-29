from django import forms
from webapp.models import Task, File


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['id', 'title', 'type', 'description', 'start_date', 'done_at', 'deadline',
                  'status', 'priority', 'parent_task', 'destination_to_department', 'destination_to_user',
                  ]

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'done_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['id', 'file']