from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse, resolve
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from logistician_app.forms import TankerForm, PlaceForm, OrderForm
from logistician_app.models import LoadOrDeliveryPlace, TankerTrailer, TransportationOrder, TrailerType
from logistician_app import views
from logistician_app.serializers import LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer, TransportationOrderSerializer
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

    def test_logistician_permission(self):
        url = reverse("order-create")
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_permission(self):
        url = reverse("order-create")
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LogisticianApp(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(username = "username1",
                                              first_name = "First",
                                              last_name = "Last",
                                              email = "test1@test.com",
                                              phone_number = 111111111,
                                              role = "Driver"
                                              )
        self.logistician = CustomUser.objects.create_user(username = "logistician",
                                                     first_name = "Logi",
                                                     last_name = "Stician",
                                                     email = "logi@test.com",
                                                     phone_number = 123456789,
                                                     role = "Logistician"
                                                     )
        self.logistician.save()
        self.logistician_group = Group.objects.create(name = "Logisticians group")
        self.logistician.groups.add(self.logistician_group)
        self.tanker = TankerTrailer.objects.create(chamber_1 = 7100,
                                                   chamber_2 = 9600,
                                                   chamber_3 = 3700,
                                                   chamber_4 = 6200,
                                                   chamber_5 = 11500
                                                   )
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
                                                        trailer_type = TrailerType.TANKER,
                                                        tanker_volume = self.tanker,
                                                        load_weight = 24000,
                                                        load_place = self.place1,
                                                        delivery_place = self.place2,
                                                        driver = self.user,
                                                        done = False
                                                        )
        self.order2 = TransportationOrder.objects.create(date = datetime.date.today(),
                                                        trailer_type = TrailerType.TIPPER,
                                                        load_weight = 22000,
                                                        load_place = self.place2,
                                                        delivery_place = self.place1,
                                                        )

    # VIEWS & TEMPLATES

    def test_get_orders_list(self):
        url = reverse("orders-list")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders_list.html")
        self.assertIn("serializer", response.context)
        self.assertIn("orders", response.context)

    def test_get_order_retrieve(self):
        order_url = reverse("order-retrieve", kwargs = {"pk": self.order.pk})
        self.client.force_login(self.logistician)
        response = self.client.get(order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_retrieve.html")
        self.assertIn("serializer", response.context)
        self.assertIn("order", response.context)
        self.assertEqual(response.context["order"], self.order)

    def test_get_archived_orders_list(self):
        url = reverse("archived-orders")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders_list.html")
        self.assertIn("serializer", response.context)
        self.assertIn("archived_orders", response.context)

    def test_get_create_order_form(self):
        url = reverse("order-create")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_form.html")
        self.assertIn("form", response.context)

    def test_post_valid_order_creation(self):
        url = reverse("order-create")
        self.client.force_login(self.logistician)
        data = {
            "date": datetime.date.today(),
            "trailer_type": TrailerType.TIPPER,
            "load_weight": 22000,
            "load_place": self.place2.id,
            "delivery_place": self.place1.id,
            "done": False
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TransportationOrder.objects.count(), 3)
        self.assertEqual(TransportationOrder.objects.first().done, False)

    def test_post_invalid_order_creation(self):
        url = reverse("order-create")
        self.client.force_login(self.logistician)
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TransportationOrder.objects.count(), 2)

    def test_get_destroy_order(self):
        url = reverse("order-destroy", kwargs={"pk": self.order.pk})
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_delete.html")
        self.assertEqual(response.context["order"], self.order)

    def test_post_destroy_order(self):
        url = reverse("order-destroy", kwargs={"pk": self.order.pk})
        self.client.force_login(self.logistician)
        response = self.client.post(url)
        self.assertRedirects(response, reverse("orders-list"))
        self.assertEqual(TransportationOrder.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Transportation order deleted successfully.")

    def test_get_places_list(self):
        url = reverse("places-list")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "places_list.html")
        self.assertEqual(len(response.context["places"]), 2)

    def test_get_single_place(self):
        self.client.force_login(self.logistician)
        response = self.client.get(reverse("place-retrieve", kwargs={"pk": self.place1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_retrieve.html")
        self.assertEqual(response.context["place"], self.place1)

    def test_get_place_create_form(self):
        url = reverse("place-create")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_form.html")
        self.assertTrue(response.context["form"].fields)

    def test_post_valid_place_creation(self):
        url = reverse("place-create")
        self.client.force_login(self.logistician)
        data = {
            "company": "Company C",
            "country": "Country C",
            "state": "State C",
            "town": "Town C",
            "postal_code": "54321",
            "street": "Street C",
            "street_number": "3",
            "contact_number": "987654321"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LoadOrDeliveryPlace.objects.count(), 3)

    def test_post_valid_place_update(self):
        self.client.force_login(self.logistician)
        data = {
            "company": "Updated Company",
            "country": "Updated Country",
            "state": "Updated State",
            "town": "Updated Town",
            "postal_code": "54321",
            "street": "Updated Street",
            "street_number": "3",
            "contact_number": "987654321"
        }
        response = self.client.post(reverse("place-update", kwargs = {"pk": self.place1.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.place1.refresh_from_db()
        self.assertEqual(self.place1.company, "Updated Company")

    def test_get_delete_place_confirmation(self):
        url = reverse("place-destroy", kwargs = {"pk": self.place1.pk})
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_delete.html")

    def test_post_place_deletion(self):
        url = reverse("place-destroy", kwargs = {"pk": self.place1.pk})
        self.client.force_login(self.logistician)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LoadOrDeliveryPlace.objects.count(), 2)

    def test_post_place_deletion_with_related_order(self):
        url = reverse("place-destroy", kwargs = {"pk": self.place1.pk})
        self.client.force_login(self.logistician)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LoadOrDeliveryPlace.objects.count(), 2)
        self.assertEqual(response.url, reverse("places-list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This place belongs to some transportation order.")

    def test_get_create_tanker_form(self):
        url = reverse("tanker-create")
        self.client.force_login(self.logistician)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tanker_form.html")

    def test_post_valid_create_tanker_form(self):
        url = reverse("tanker-create")
        self.client.force_login(self.logistician)
        data = {
            "chamber_1": 6000,
            "chamber_2": 8000,
            "chamber_3": 3600,
            "chamber_4": 6000,
            "chamber_5": 11000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TankerTrailer.objects.count(), 2)
        self.assertEqual(response.url, reverse("order-create"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Tanker trailer volumes set up successfully.")

    def test_post_invalid_create_tanker_form(self):
        url = reverse("tanker-create")
        self.client.force_login(self.logistician)
        data = {
            "chamber_1": -1000,
            "chamber_2": 8000,
            "chamber_3": 4000,
            "chamber_4": 7000,
            "chamber_5": 11000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TankerTrailer.objects.count(), 1)
        self.assertTemplateUsed(response, "tanker_form.html")

    def test_get_update_tanker_form(self):
        self.client.force_login(self.logistician)
        update_url = reverse("tanker-update", kwargs = {"pk": self.tanker.pk})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tanker_form.html")

    def test_post_valid_update_tanker_form(self):
        self.client.force_login(self.logistician)
        update_url = reverse("tanker-update", kwargs = {"pk": self.tanker.pk})
        data = {
            "chamber_1": 6000,
            "chamber_2": 8000,
            "chamber_3": 3500,
            "chamber_4": 5000,
            "chamber_5": 11000,
        }
        response = self.client.post(update_url, data)
        self.assertEqual(response.status_code, 302)
        self.tanker.refresh_from_db()
        self.assertEqual(self.tanker.chamber_1, 6000)
        self.assertEqual(self.tanker.chamber_2, 8000)
        self.assertEqual(self.tanker.chamber_3, 3500)
        self.assertEqual(self.tanker.chamber_4, 5000)
        self.assertEqual(self.tanker.chamber_5, 11000)
        self.assertEqual(response.url, reverse("orders-list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Tanker trailer volumes updated successfully.")

    def test_post_invalid_update_tanker_form(self):
        self.client.force_login(self.logistician)
        update_url = reverse("tanker-update", kwargs = {"pk": self.tanker.pk})
        data = {
            "chamber_1": 8000,
            "chamber_2": 10000,
            "chamber_3": -4000,
            "chamber_4": 7000,
            "chamber_5": 12000,
        }
        response = self.client.post(update_url, data)
        self.assertEqual(response.status_code, 400)
        self.tanker.refresh_from_db()
        self.assertEqual(self.tanker.chamber_1, 7100)
        self.assertEqual(self.tanker.chamber_2, 9600)
        self.assertEqual(self.tanker.chamber_3, 3700)
        self.assertEqual(self.tanker.chamber_4, 6200)
        self.assertEqual(self.tanker.chamber_5, 11500)
        self.assertTemplateUsed(response, "tanker_form.html")

    # MODELS

    def test_transportation_order_model(self):
        self.assertEqual(self.order.date, datetime.date.today())
        self.assertEqual(self.order.trailer_type, TrailerType.TANKER)
        self.assertEqual(self.order.tanker_volume, self.tanker)
        self.assertEqual(self.order.load_weight, 24000)
        self.assertEqual(self.order.load_place, self.place1)
        self.assertEqual(self.order.delivery_place, self.place2)
        self.assertEqual(self.order.driver, self.user)
        self.assertEqual(self.order.done, False)
        self.assertEqual(TransportationOrder.objects.count(), 2)

    def test_place_restrict_with_different_places(self):
        load_place = self.place1
        delivery_place = self.place2
        try:
            your_instance = TransportationOrder(date = datetime.date.today(),
                                                trailer_type = TrailerType.TANKER,
                                                tanker_volume = self.tanker,
                                                load_weight = 24000,
                                                load_place = load_place,
                                                delivery_place = delivery_place,
                                                )
            your_instance.place_restrict()
        except Exception:
            self.fail("place_restrict raised Exception unexpectedly")

    def test_place_restrict_with_same_places(self):
        load_place = self.place1
        delivery_place = self.place1
        your_instance = TransportationOrder(date = datetime.date.today(),
                                            trailer_type = TrailerType.TANKER,
                                            tanker_volume = self.tanker,
                                            load_weight = 24000,
                                            load_place = load_place,
                                            delivery_place = delivery_place,
                                            )
        with self.assertRaises(Exception):
            your_instance.place_restrict()

    def test_empty_tanker_volume_with_tanker_trailer_and_no_volume(self):
        order = TransportationOrder.objects.create(date = datetime.date.today(),
                                                   trailer_type = TrailerType.TANKER,
                                                   load_weight = 24000,
                                                   load_place = self.place1,
                                                   delivery_place = self.place2,
                                                   )
        with self.assertRaises(Exception):
            order.empty_tanker_volume()

    def test_empty_tanker_volume_with_non_tanker_trailer(self):
        order = TransportationOrder.objects.create(date = datetime.date.today(),
                                                   trailer_type = TrailerType.INSULATED,
                                                   tanker_volume = self.tanker,
                                                   load_weight = 24000,
                                                   load_place = self.place1,
                                                   delivery_place = self.place2,
                                                   )
        try:
            order.empty_tanker_volume()
        except Exception:
            self.fail("empty_tanker_volume raised Exception unexpectedly")

    def test_place_model(self):
        self.assertEqual(self.place1.company, "Test 1")
        self.assertEqual(self.place1.country, "Poland")
        self.assertEqual(self.place1.state, "Mazowieckie")
        self.assertEqual(self.place1.town, "Warszawa")
        self.assertEqual(self.place1.postal_code, "00-000")
        self.assertEqual(self.place1.street, "Mazowiecka")
        self.assertEqual(self.place1.street_number, 1)
        self.assertEqual(self.place1.contact_number, 111111111)
        self.assertEqual(LoadOrDeliveryPlace.objects.count(), 2)

    def test_company_is_unique(self):
        with self.assertRaises(IntegrityError):
            LoadOrDeliveryPlace.objects.create(company = "Test 1",
                                               country = "Germany",
                                               state = "Brandenburg",
                                               town = "Berlin",
                                               postal_code = "11-111",
                                               street = "Berliner Strasse",
                                               street_number = 2,
                                               contact_number = 222222222
                                               )

    def test_get_volume(self):
        trailer = TankerTrailer(chamber_1 = 500, chamber_2 = 1000, chamber_3 = 1500, chamber_4 = 2000, chamber_5 = 2500)
        self.assertEqual(trailer.get_volume(), 7500)

    def test_get_volume_with_none_values(self):
        trailer = TankerTrailer(chamber_1 = None, chamber_2 = 1000, chamber_3 = None, chamber_4 = 2000, chamber_5 = None)
        self.assertEqual(trailer.get_volume(), 3000)

    def test_get_volume_with_zero_values(self):
        trailer = TankerTrailer(chamber_1 = 0, chamber_2 = 0, chamber_3 = 0, chamber_4 = 0, chamber_5 = 0)
        self.assertEqual(trailer.get_volume(), 0)

    def test_negative_value_raises_validation_error(self):
        trailer = TankerTrailer(chamber_1=-8000)
        with self.assertRaises(IntegrityError):
            trailer.save()

    def test_exceeding_max_value_raises_validation_error(self):
        trailer = TankerTrailer()
        with self.assertRaises(ValidationError):
            trailer.chamber_2 = 10000
            trailer.full_clean()

    def test_blank_value_is_allowed(self):
        trailer = TankerTrailer(chamber_1 = None)
        self.assertIsNone(trailer.chamber_1)

    def test_default_value(self):
        trailer = TankerTrailer()
        self.assertEqual(trailer.chamber_1, 0)

    # FORMS

    def test_order_form_valid_data(self):
        data = {
            'date': datetime.date.today(),
            'trailer_type': TrailerType.TANKER,
            'load_place': self.place1,
            'tanker_volume': self.tanker,
            'load_weight': 24000,
            'delivery_place': self.place2
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_order_form_missing_data(self):
        data = {
            'date': datetime.date.today(),
            'trailer_type': TrailerType.TANKER,
            'tanker_volume': 5000,
            'load_weight': 24000,
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())

    def test_place_form_valid_data(self):
        data = {
            'company': 'Test Company',
            'country': 'Poland',
            'state': 'Mazowieckie',
            'town': 'Warszawa',
            'postal_code': '00-000',
            'street': 'Mazowiecka',
            'street_number': '1',
            'contact_number': '111111111'
        }
        form = PlaceForm(data)
        self.assertTrue(form.is_valid())

    def test_place_form_missing_data(self):
        data = {
            'company': 'Test Company',
            'country': 'Poland',
            'state': 'Mazowieckie',
            'town': 'Warszawa',
            'postal_code': '00-000',
        }
        form = PlaceForm(data)
        self.assertFalse(form.is_valid())

    def test_tanker_form_valid_data(self):
        data = {
            'chamber_1': 1000,
            'chamber_2': 2000,
            'chamber_3': 3000,
            'chamber_4': 4000,
            'chamber_5': 5000
        }
        form = TankerForm(data)
        self.assertTrue(form.is_valid())

    def test_tanker_form_invalid_data(self):
        data = {
            'chamber_1': 8000,
            'chamber_2': 2000,
            'chamber_3': 3000,
            'chamber_4': 4000,
            'chamber_5': -5000
        }
        form = TankerForm(data)
        self.assertFalse(form.is_valid())

    # URLS

    def test_orders_list_url(self):
        url = reverse('orders-list')
        self.assertEqual(resolve(url).func.view_class, views.TransportationOrderView)

    def test_order_retrieve_url(self):
        url = reverse('order-retrieve', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.TransportationOrderView)

    def test_order_create_url(self):
        url = reverse('order-create')
        self.assertEqual(resolve(url).func.view_class, views.TransportationOrderCreateOrUpdateView)

    def test_order_update_url(self):
        url = reverse('order-update', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.TransportationOrderCreateOrUpdateView)

    def test_order_destroy_url(self):
        url = reverse('order-destroy', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.TransportationOrderDestroyView)

    def test_archived_orders_list_url(self):
        url = reverse('archived-orders')
        self.assertEqual(resolve(url).func.view_class, views.ArchivedTransportationOrderView)

    def test_places_list_url(self):
        url = reverse('places-list')
        self.assertEqual(resolve(url).func.view_class, views.PlaceView)

    def test_place_retrieve_url(self):
        url = reverse('place-retrieve', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.PlaceView)

    def test_place_create_url(self):
        url = reverse('place-create')
        self.assertEqual(resolve(url).func.view_class, views.PlaceCreateOrUpdateView)

    def test_place_update_url(self):
        url = reverse('place-update', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.PlaceCreateOrUpdateView)

    def test_place_destroy_url(self):
        url = reverse('place-destroy', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.PlaceDestroyView)

    def test_tanker_create_url(self):
        url = reverse('tanker-create')
        self.assertEqual(resolve(url).func.view_class, views.TankerCreateOrUpdateView)

    def test_tanker_update_url(self):
        url = reverse('tanker-update', args = [1])
        self.assertEqual(resolve(url).func.view_class, views.TankerCreateOrUpdateView)

    # MANAGERS

    def test_current_order_manager(self):
        TransportationOrder.objects.create(date = datetime.date.today(),
                                           trailer_type = TrailerType.TIPPER,
                                           load_weight = 22000,
                                           load_place = self.place2,
                                           delivery_place = self.place1,
                                           done = False
                                           )
        TransportationOrder.objects.create(date = datetime.date.today(),
                                           trailer_type = TrailerType.TIPPER,
                                           load_weight = 22000,
                                           load_place = self.place2,
                                           delivery_place = self.place1,
                                           done = False
                                           )
        TransportationOrder.objects.create(date = datetime.date.today(),
                                           trailer_type = TrailerType.TIPPER,
                                           load_weight = 22000,
                                           load_place = self.place2,
                                           delivery_place = self.place1,
                                           done = True
                                           )
        TransportationOrder.objects.create(date = datetime.date.today(),
                                           trailer_type = TrailerType.TIPPER,
                                           load_weight = 22000,
                                           load_place = self.place2,
                                           delivery_place = self.place1,
                                           done = False
                                           )
        TransportationOrder.objects.create(date = datetime.date.today(),
                                           trailer_type = TrailerType.TIPPER,
                                           load_weight = 22000,
                                           load_place = self.place2,
                                           delivery_place = self.place1,
                                           done = True
                                           )
        current_orders = TransportationOrder.current.all()
        archived_orders = TransportationOrder.archived.all()
        self.assertEqual(current_orders.count(), 5)
        self.assertEqual(archived_orders.count(), 2)
        for order in current_orders:
            self.assertFalse(order.done)
        for order in archived_orders:
            self.assertTrue(order.done)

    # SERIALIZERS

    def test_load_or_delivery_place_serializer(self):
        serializer = LoadOrDeliveryPlaceSerializer(instance = self.place1)
        self.assertEqual(serializer.data['company'], self.place1.company)
        self.assertEqual(serializer.data['country'], self.place1.country)
        self.assertEqual(serializer.data['state'], self.place1.state)
        self.assertEqual(serializer.data['town'], self.place1.town)
        self.assertEqual(serializer.data['postal_code'], self.place1.postal_code)
        self.assertEqual(serializer.data['street'], self.place1.street)
        self.assertEqual(serializer.data['street_number'], self.place1.street_number)
        self.assertEqual(serializer.data['contact_number'], self.place1.contact_number)

    def test_tanker_trailer_serializer(self):
        serializer = TankerTrailerSerializer(instance = self.tanker)
        self.assertEqual(serializer.data['chamber_1'], self.tanker.chamber_1)
        self.assertEqual(serializer.data['chamber_2'], self.tanker.chamber_2)
        self.assertEqual(serializer.data['chamber_3'], self.tanker.chamber_3)
        self.assertEqual(serializer.data['chamber_4'], self.tanker.chamber_4)
        self.assertEqual(serializer.data['chamber_5'], self.tanker.chamber_5)

    def test_transportation_order_serializer(self):
        serializer = TransportationOrderSerializer(instance = self.order)
        self.assertEqual(serializer.data['date'], str(self.order.date))
        self.assertEqual(serializer.data['trailer_type'], self.order.trailer_type)
        self.assertEqual(serializer.data['tanker_volume']['chamber_1'], self.tanker.chamber_1)
        self.assertEqual(serializer.data['load_weight'], self.order.load_weight)
        self.assertEqual(serializer.data['load_place']['company'], self.place1.company)
        self.assertEqual(serializer.data['delivery_place']['company'], self.place2.company)
        self.assertEqual(serializer.data['driver']['username'], self.user.username)
        self.assertEqual(serializer.data['done'], self.order.done)


