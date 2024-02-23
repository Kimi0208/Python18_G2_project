from django import forms
from django.forms import widgets
from webapp.models import Status, Task, Priority
from accounts.models import Department, DefUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'deadline', 'status', 'author', 'destination_to_department',
                  'destination_to_user', 'files')
    title = forms.CharField(max_length=100, required=True, label="Название задачи")
    description = forms.CharField(
        max_length=3000, required=False, label="Описание задачи", widget=widgets.Textarea
    )
    # deadline = forms.DateField
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    priority = forms.ModelChoiceField(queryset=Priority.objects.all())
    widgets = {
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'})
    }
    # author = forms.CharField(max_length=100, required=True, label="Автор задачи")
    destination_to_department = forms.ModelChoiceField(queryset=Department.objects.all())
    destination_to_user = forms.ModelChoiceField(queryset=DefUser.objects.all())
    files = forms.FileField(required=False)
