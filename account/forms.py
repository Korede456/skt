from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class CustomUserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'password1', 'password2']



class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
