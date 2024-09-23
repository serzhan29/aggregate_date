from .models import TeacherReport
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=63)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class TeacherReportForm(forms.ModelForm):
    class Meta:
        model = TeacherReport
        fields = ['plan_2022_2023', 'actual_2023_2024', 'plan_2024_2025', 'comment']

