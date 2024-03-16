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
        'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'email_password', 'phone_number')
        labels = {'username': 'Логин', 'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email',
                  'phone_number': 'Номер телефона', 'email_password': 'Пароль от почтового ящика'}


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'email_password', 'phone_number']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email',
                  'email_password': 'Пароль от почтового ящика', 'phone_number': 'Номер телефона'}


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
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'position')
    username = forms.CharField(max_length=50, required=True, label="Логин")
    first_name = forms.CharField(max_length=50, required=True, label="Имя")
    last_name = forms.CharField(max_length=50, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(required=True, label="Номер телефона")
    position = forms.ModelChoiceField(queryset=Position.objects.all(), label="Должность")
