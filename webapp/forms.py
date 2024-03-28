from django import forms
from webapp.models import Task, Comment, CompaniesList, InOutMails


class TaskForm(forms.ModelForm):
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'input-file', 'style': 'width: 50%'}))

    class Meta:
        model = Task
        fields = ['title', 'type', 'description', 'start_date', 'done_at', 'deadline', 'attachment',
                  'status', 'priority', 'parent_task', 'destination_to_department', 'destination_to_user',
                  ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 50%'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 50%'}),
        }

        for i in fields:
            if i not in ('title', 'description', 'start_date', 'done_at', 'deadline'):
                widgets[i] = forms.Select(attrs={'class': 'form-control', 'style': 'width: 50%'})
        for i in ('start_date', 'done_at', 'deadline'):
            widgets[i] = forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width: 50%'})

        def __init__(self, *args, **kwargs):
            super(TaskForm, self).__init__(*args, **kwargs)
            if not self.instance.pk:
                self.fields.pop('status', None)


# class UploadFileForm(forms.Form):
#     file = forms.FileField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']


class CompaniesListForm(forms.ModelForm):
    class Meta:
        model = CompaniesList
        fields = ['company_code', 'company_name', 'company_inn']


class InOutMailsForm(forms.ModelForm):
    class Meta:
        model = InOutMails
        fields = ['mail_number', 'input_mail_number', 'sender_name', 'mail_description',
                  'pages_count', 'responsible_department', 'responsible_employee', 'attachment', 'status', 'type']

