from django import forms
from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'type', 'description', 'start_date', 'done_at', 'deadline',
                  'status', 'priority', 'parent_task', 'destination_to_department', 'destination_to_user',
                  ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 50%' }),
            'description': forms.Textarea(attrs={'class': 'form-control','style': 'width: 50%' })
        }
        for i in fields:
            if i not in ('title', 'description', 'start_date', 'done_at', 'deadline'):
                widgets[i] = forms.Select(attrs={'class': 'form-control','style': 'width: 50%'})
        for i in ('start_date', 'done_at', 'deadline'):
            widgets[i] = forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width: 50%'})
