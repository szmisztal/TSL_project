from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from dispatcher_app.forms import AssignForm
from dispatcher_app.views import assign_order_to_driver, OrdersListView
from logistician_app.models import LoadOrDeliveryPlace, TransportationOrder, TrailerType
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

    def test_dispatcher_permission(self):
        url = reverse("assign-order")
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_permission(self):
        url = reverse("assign-order")
        self.client.force_login(self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DispatcherAppTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.driver = CustomUser.objects.create_user(username = "driver1",
                                                     password = "P455word!",
                                                     first_name = "Driver",
                                                     last_name = "One",
                                                     email = "driver1@example.com",
                                                     phone_number = 000000000,
                                                     role = "Driver"
                                                     )
        self.dispatcher = CustomUser.objects.create_user(username = "dispatcher1",
                                                   password = "P455word!",
                                                   first_name = "Dispatcher",
                                                   last_name = "One",
                                                   email = "dispatcher1@example.com",
                                                   phone_number = 999999999,
                                                   role = "Dispatcher"

        )
        self.dispatcher_group = Group.objects.create(name = "Dispatchers group")
        self.dispatcher.groups.add(self.dispatcher_group)
        self.place1 = LoadOrDeliveryPlace.objects.create(company = "Test 1",
                                                         country = "Poland",
                                                         state = "Mazowieckie",
                                                         town = "Warszawa",
                                                         postal_code = "00-000",
                                                         street = "Mazowiecka",
                                                         street_number = "1",
                                                         contact_number = 111111111
                                                         )
        self.place2 = LoadOrDeliveryPlace.objects.create(company = "Test 2",
                                                         country = "Germany",
                                                         state = "Brandenburg",
                                                         town = "Berlin",
                                                         postal_code = "11-111",
                                                         street = "Berliner Strasse",
                                                         street_number = "2",
                                                         contact_number = 222222222
                                                         )
        self.order = TransportationOrder.objects.create(date = datetime.date.today(),
                                                        trailer_type = TrailerType.TIPPER,
                                                        load_weight = 24000,
                                                        load_place = self.place1,
                                                        delivery_place = self.place2,
                                                        )

    # FORMS

    def test_valid_form(self):
        form = AssignForm(instance = self.order, data = {"driver": self.driver.id})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = AssignForm(instance = self.order)
        self.assertFalse(form.is_valid())

    # URLS

    def test_assign_order_url(self):
        url = reverse("assign-order")
        self.assertEqual(resolve(url).func.view_class, OrdersListView)

    def test_make_assign_url(self):
        url = reverse("make-assign", kwargs={"pk": self.order.pk})
        self.assertEqual(url, f"/dispatcher/make_assign/{self.order.pk}/")

    # VIEWS & TEMPLATES

    def test_assign_order_to_driver_view_get(self):
        url = reverse("make-assign", kwargs = {"pk": self.order.pk})
        self.client.force_login(self.dispatcher)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assign_order_form.html")

    def test_assign_order_to_driver_view_post_valid(self):
        url = reverse("make-assign", kwargs = {"pk": self.order.pk})
        self.client.force_login(self.dispatcher)
        driver = self.driver
        response = self.client.post(url, {"driver": driver.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("assign-order"))
        self.order.refresh_from_db()
        self.assertEqual(self.order.driver, driver)

    def test_assign_order_to_driver_view_post_invalid(self):
        url = reverse("make-assign", kwargs = {"pk": self.order.pk})
        self.client.force_login(self.dispatcher)
        response = self.client.post(url, data = {"driver": ""})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("assign-order"))
        self.order.refresh_from_db()
        self.assertIsNone(self.order.driver)

    def test_assign_order_to_driver_view_invalid_order(self):
        invalid_order_pk = self.order.pk + 100
        url = reverse("make-assign", kwargs = {"pk": invalid_order_pk})
        self.client.force_login(self.dispatcher)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("assign-order"))
