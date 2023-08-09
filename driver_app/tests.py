from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse, resolve
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from driver_app.forms import OrderDoneForm
from driver_app.views import CurrentOrder, send_emails
from logistician_app.models import TransportationOrder, LoadOrDeliveryPlace, TrailerType
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

class DriverAppTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username = "username",
                                                   first_name = "First",
                                                   last_name = "Last",
                                                   email = "test@test.com",
                                                   phone_number = 333333333,
                                                   role = "Driver"
                                                   )
        self.user.save()
        self.driver_group = Group.objects.create(name = "Drivers group")
        self.user.groups.add(self.driver_group)
        self.place1 = LoadOrDeliveryPlace.objects.create(company = "Test 1",
                                                         country = "Poland",
                                                         state = "Mazowieckie",
                                                         town = "Warszawa",
                                                         postal_code = "00-000",
                                                         street = "Mazowiecka",
                                                         street_number = 1,
                                                         contact_number = 111111111
                                                         )
        self.place2 = LoadOrDeliveryPlace.objects.create(company = "Test 2",
                                                         country = "Germany",
                                                         state = "Brandenburg",
                                                         town = "Berlin",
                                                         postal_code = "11-111",
                                                         street = "Berliner Strasse",
                                                         street_number = 2,
                                                         contact_number = 222222222
                                                         )
        self.order = TransportationOrder.objects.create(date = datetime.date.today(),
                                                        trailer_type = TrailerType.TIPPER,
                                                        load_weight = 24000,
                                                        load_place = self.place1,
                                                        delivery_place = self.place2,
                                                        driver = self.user
                                                        )

    # FORMS

    def test_valid_form(self):
        data = {'done': True}
        form = OrderDoneForm(data = data, instance = self.order)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'done': None}
        form = OrderDoneForm(data = data, instance = self.order)
        self.assertFalse(form.is_valid())

    # URLS

    def test_current_order_url(self):
        url = reverse("current-order")
        self.assertEqual(resolve(url).func.view_class, CurrentOrder)

    # VIEWS & TEMPLATES

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("current-order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "driver_order_form.html")

    def test_post_valid_form(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("current-order"), {"done": True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("homepage"))

    def test_post_invalid_form(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("current-order"), {"done": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "driver_order_form.html")

    def test_send_emails(self):
        user1 = CustomUser.objects.create(
            username = "dispatcher1",
            password = "P455word!",
            first_name = "Dispatcher",
            last_name = "One",
            email = "dispatcher1@example.com",
            phone_number = 444444444,
            role = "Dispatcher"
        )
        request = self.client.request()
        request.user = self.user
        mail.outbox = []
        send_emails(request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "ORDER FINISHED")
        self.assertIn(f"{self.user.first_name} {self.user.last_name} has finished his order.", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].from_email, "sz.misztal@gmail.com")
        self.assertIn("dispatcher1@example.com", mail.outbox[0].to)



