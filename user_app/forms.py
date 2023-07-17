from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 64)
    password = forms.CharField(max_length = 64, widget = forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'role']
