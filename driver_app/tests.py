from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_app.models import CustomUser

# PERMISSIONS
class PermissionsTest(APITestCase):

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
        self.logistician_group = Group.objects.create(name = "Logisticians group")
        self.dispatcher_group = Group.objects.create(name = "Dispatchers group")
        self.driver_group = Group.objects.create(name = "Drivers group")

        self.user1.groups.add(self.logistician_group)
        self.user2.groups.add(self.dispatcher_group)
        self.user3.groups.add(self.driver_group)

    def test_driver_permission(self):
        url = reverse("current-order")
        self.client.force_login(self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_permission(self):
        url = reverse("current-order")
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

