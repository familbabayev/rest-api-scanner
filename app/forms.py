from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Incorrect email or password.',
    }
