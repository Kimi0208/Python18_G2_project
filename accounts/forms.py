from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

from accounts.models import DefUser


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Новый пароль')
    password2 = forms.CharField(label='Подтверждение пароля')

    class Meta(UserCreationForm.Meta):
        model = DefUser
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'email_password', 'phone_number')
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email',
                  'phone_number': 'Номер телефона', 'email_password': 'Пароль от почтового ящика'}


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email', 'phone_number': 'Номер телефона'}


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