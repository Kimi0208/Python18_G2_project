from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from accounts.models import DefUser, Position, Department


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Новый пароль')
    password2 = forms.CharField(label='Подтверждение пароля')

    class Meta(UserCreationForm.Meta):
        model = DefUser
        fields = (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number')
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'patronymic': 'Отчество', 'email': 'Email',
                  'phone_number': 'Номер телефона'}


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = DefUser
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone_number']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'patronymic': 'Отчество', 'email': 'Email',
                  'phone_number': 'Номер телефона'}


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput,
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = DefUser
        fields = ('username', 'password', 'first_name', 'last_name', 'patronymic', 'email', 'position', 'phone_number')
    username = forms.CharField(max_length=50, required=True, label="Логин")
    password = forms.CharField(max_length=250, required=True, label="Пароль")
    first_name = forms.CharField(max_length=50, required=True, label="Имя")
    last_name = forms.CharField(max_length=50, required=True, label="Фамилия")
    patronymic = forms.CharField(max_length=50, label="Отчество", required=False)
    email = forms.EmailField(required=True, label="Email", max_length=5000)
    phone_number = forms.CharField(required=True, label="Номер телефона")
    position = forms.ModelChoiceField(queryset=Position.objects.all(), label="Должность")



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)
        labels = {'name': 'Отдел'}

