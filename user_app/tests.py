from django.test import TestCase, Client
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from .models import CustomUser

class User_app_test(TestCase):

    # FORMS

    def test_registration_form_valid_data(self):
        data = {
            "username": "username",
            "password1": "p455word!",
            "password2": "p455word!",
            "first_name": "Name",
            "last_name": "Surname",
            "email": "email@email.com",
            "phone_number": 111222333,
            "role": "Driver"
        }
        form = RegisterForm(data = data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_data(self):
        invalid_data = {
            "username": "",
            "password1": "password123",
            "password2": "password456",
            "first_name": "Name",
            "last_name": "Surname",
            "email": "invalid_email",
            "phone_number": "",
            "role": "InvalidRole"
        }
        form = RegisterForm(data = invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_registration_form_missing_fields(self):
        form = RegisterForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)

    def test_login_form_valid_data(self):
        data = {
            "username": "username",
            "password": "p455word!"
        }
        form = LoginForm(data = data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_fields(self):
        invalid_data = {
            "username": "username",
            "password": ""
        }
        form = LoginForm(data = invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    # URLS & TEMPLATES




