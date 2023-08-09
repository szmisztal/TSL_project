from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import Group

from TSL_project.views import HomepageView
from user_app.models import CustomUser

class HomepageViewTest(TestCase):

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

        logistician_group = Group.objects.create(name = "Logisticians group")
        dispatcher_group = Group.objects.create(name = "Dispatchers group")
        driver_group = Group.objects.create(name = "Drivers group")

        self.user1.groups.add(logistician_group)
        self.user2.groups.add(dispatcher_group)
        self.user3.groups.add(driver_group)

    # VIEWS

    def test_logistician_context(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_logistician"], True)
        self.assertEqual(response.context["is_dispatcher"], False)
        self.assertEqual(response.context["is_driver"], False)

    def test_dispatcher_context(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_logistician"], False)
        self.assertEqual(response.context["is_dispatcher"], True)
        self.assertEqual(response.context["is_driver"], False)

    def test_driver_context(self):
        self.client.force_login(self.user3)
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["is_logistician"], False)
        self.assertEqual(response.context["is_dispatcher"], False)
        self.assertEqual(response.context["is_driver"], True)

    # URLS

    def test_homepage_url(self):
        url = reverse("homepage")
        self.assertEqual(resolve(url).func.view_class, HomepageView)

    def test_admin_url(self):
        url = "/admin/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_users_url(self):
        self.client.force_login(self.user1)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logistician_url(self):
        self.client.force_login(self.user1)
        url = reverse("orders-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dispatcher_url(self):
        self.client.force_login(self.user2)
        url = reverse("assign-order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_driver_url(self):
        self.client.force_login(self.user3)
        url = reverse("current-order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
