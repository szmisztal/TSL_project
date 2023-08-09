from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from .serializers import UserSerializer
from .views import sign_up, sign_in, sign_out

class UserAppTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(username = "username1",
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "test1@test.com",
                                              phone_number = 111111111,
                                              role = "Logistician"
                                              )
        self.user2 = CustomUser.objects.create(username = "username2",
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "test2@test.com",
                                              phone_number = 222222222,
                                              role = "Dispatcher"
                                              )
        self.user3 = CustomUser.objects.create(username = "username3",
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "test3@test.com",
                                              phone_number = 333333333,
                                              role = "Driver"
                                              )
        self.user4 = CustomUser.objects.create(username = "username6",
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "test6@test.com",
                                              phone_number = 666666666,
                                              role = "Driver"
                                              )
        self.logistician_group = Group.objects.create(name = "Logisticians group")
        self.dispatcher_group = Group.objects.create(name = "Dispatchers group")
        self.driver_group = Group.objects.create(name = "Drivers group")
        self.non_driver = CustomUser.objects.get(username = self.user1.username)

    # MODELS

    def test_custom_user_model(self):
        self.assertEqual(self.user1.username, "username1")
        self.assertEqual(self.user1.first_name, "First")
        self.assertEqual(self.user1.last_name, "Last")
        self.assertEqual(self.user1.email, "test1@test.com")
        self.assertEqual(self.user1.phone_number, 111111111)
        self.assertEqual(self.user1.role, "Logistician")
        self.assertEqual(CustomUser.objects.count(), 4)

    def test_username_is_unique(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username = "username1",
                                      first_name = "First",
                                      last_name = "Last",
                                      email = "test4@test.com",
                                      phone_number = 444444444,
                                      role = "Driver"
                                      )

    def test_email_is_unique(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username = "username4",
                                      first_name = "First",
                                      last_name = "Last",
                                      email = "test1@test.com",
                                      phone_number = 555555555,
                                      role = "Driver"
                                      )

    def test_phone_number_is_unique(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username = "username5",
                                      first_name = "First",
                                      last_name = "Last",
                                      email = "test5@test.com",
                                      phone_number = 111111111,
                                      role = "Driver"
                                      )

    def test_set_group_logistician(self):
        self.user1.set_group()
        self.assertTrue(self.user1.groups.filter(name = "Logisticians group").exists())
        self.assertFalse(self.user1.groups.filter(name = "Dispatchers group").exists())
        self.assertFalse(self.user1.groups.filter(name = "Drivers group").exists())

    def test_set_group_dispatcher(self):
        self.user2.set_group()
        self.assertFalse(self.user2.groups.filter(name = "Logisticians group").exists())
        self.assertTrue(self.user2.groups.filter(name = "Dispatchers group").exists())
        self.assertFalse(self.user2.groups.filter(name = "Drivers group").exists())

    def test_set_group_driver(self):
        self.user3.set_group()
        self.assertFalse(self.user3.groups.filter(name = "Logisticians group").exists())
        self.assertFalse(self.user3.groups.filter(name = "Dispatchers group").exists())
        self.assertTrue(self.user3.groups.filter(name = "Drivers group").exists())

    def test_create_auth_token(self):
        token = Token.objects.get(user = self.user1)
        self.assertIsNotNone(token)

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

    # URLS

    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, sign_up)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, sign_in)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, sign_out)

    # VIEWS & TEMPLATES

    def test_register_view(self):
        client = Client()
        response = client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_login_view(self):
        client = Client()
        response = client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_users_list_view_authenticated(self):
        self.client.force_login(self.user1)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "users_list.html")

        users = response.context["users"]
        self.assertEqual(len(users), 4)

    def test_users_list_view_unauthenticated(self):
        url = reverse("users-list")
        expected_redirect_url = reverse("login") + "?next=" + url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect_url)

    # MANAGERS

    def test_driver_manager_returns_drivers(self):
        drivers = CustomUser.drivers.all()
        self.assertEqual(drivers.count(), 2)
        self.assertIn(self.user3, drivers)
        self.assertIn(self.user4, drivers)
        self.assertNotIn(self.non_driver, drivers)

    def test_driver_manager_empty_result(self):
        CustomUser.objects.all().delete()
        drivers = CustomUser.drivers.all()
        self.assertEqual(drivers.count(), 0)

    def test_driver_manager_non_driver_role(self):
        non_drivers = CustomUser.drivers.filter(role = "Dispatcher")
        self.assertEqual(non_drivers.count(), 0)

    # SERIALIZERS

    def test_serializer_create_user(self):
        self.raw_password = "P455word!"
        self.data = {
            "username": "testuser",
            "password": self.raw_password,
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@email.com",
            "phone_number": 987654321,
            "role": "Driver"
        }
        self.serializer = UserSerializer(data=self.data)
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)
        user = self.serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, self.data["username"])
        self.assertEqual(user.first_name, self.data["first_name"])
        self.assertEqual(user.last_name, self.data["last_name"])
        self.assertEqual(user.email, self.data["email"])
        self.assertEqual(user.phone_number, self.data["phone_number"])
        self.assertEqual(user.role, self.data["role"])
        self.assertNotEqual(user.password, self.raw_password)

    def test_serializer_login(self):
        self.raw_password = "P455word!"
        user5 = CustomUser.objects.create_user(
            username = "testuser",
            password = self.raw_password,
            first_name = "Test",
            last_name = "User",
            email = "testuser@email.com",
            phone_number = 987654321,
            role = "Driver"
        )
        self.assertTrue(user5.check_password(self.raw_password))


