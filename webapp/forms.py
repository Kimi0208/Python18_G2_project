from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Task, File, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'type', 'description', 'start_date', 'deadline',
                  'status', 'priority', 'destination_to_department', 'destination_to_user',
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

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields.pop('status', None)

    def clean(self):
        cleaned_data = super().clean()
        destination_to_user = cleaned_data.get('destination_to_user')
        destination_to_department = cleaned_data.get('destination_to_department')
        if destination_to_user and destination_to_department:
            raise ValidationError(
                'Можно заполнить только одно из полей! \n'
                ' "На какого сотрудника задача" или "На какой отдел задача"')

        if not destination_to_user and not destination_to_department:
            raise ValidationError(
                'Необходимо заполнить хотя бы одно из полей! \n'
                '"На какого сотрудника задача" или "На какой отдел задача"')
        return cleaned_data


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['id', 'file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['id', 'description']

