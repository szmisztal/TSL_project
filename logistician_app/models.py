from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_app.models import CustomUser
import datetime
from .managers import CurrentOrderManager, ArchivedOrderManager

class TrailerType(models.TextChoices):
    CURTAIN_SIDE = "Curtain-side trailer"
    REFRIGERATED = "Refrigerated trailer"
    TIPPER = "Tipper trailer"
    LOW_LOADER = "Low-loader trailer"
    CONTAINER = "Container trailer"
    TANKER = "Tanker trailer"
    SELF_UNLOADING = "Self-unloading trailer"
    INSULATED = "Insulated trailer"

class LoadOrDeliveryPlace(models.Model):
    company = models.CharField(max_length = 64, unique = True)
    country = models.CharField(max_length = 64)
    state = models.CharField(max_length = 64)
    town = models.CharField(max_length = 64)
    postal_code = models.CharField(max_length = 16)
    street = models.CharField(max_length = 64)
    street_number = models.PositiveSmallIntegerField()
    contact_number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.country} - {self.state} - {self.town} {self.postal_code}, st. {self.street} {self.street_number}." \
               f" Company: {self.company}, Contact: {self.contact_number}."

class TankerTrailer(models.Model):
    chamber_1 = models.PositiveSmallIntegerField(blank = True, null = True, default = 0, validators = [MaxValueValidator(7100)])
    chamber_2 = models.PositiveSmallIntegerField(blank = True, null = True, default = 0, validators = [MaxValueValidator(9600)])
    chamber_3 = models.PositiveSmallIntegerField(blank = True, null = True, default = 0, validators = [MaxValueValidator(3700)])
    chamber_4 = models.PositiveSmallIntegerField(blank = True, null = True, default = 0, validators = [MaxValueValidator(6200)])
    chamber_5 = models.PositiveSmallIntegerField(blank = True, null = True, default = 0, validators = [MaxValueValidator(11500)])

    def get_volume(self):
        whole_volume = 0
        if self.chamber_1 is not None:
            whole_volume += self.chamber_1
        if self.chamber_2 is not None:
            whole_volume += self.chamber_2
        if self.chamber_3 is not None:
            whole_volume += self.chamber_3
        if self.chamber_4 is not None:
            whole_volume += self.chamber_4
        if self.chamber_5 is not None:
            whole_volume += self.chamber_5
        return whole_volume

    def __str__(self):
        return f"{self.chamber_1} + {self.chamber_2} + {self.chamber_3} + {self.chamber_4} + {self.chamber_5} = " + str(self.get_volume())

class TransportationOrder(models.Model):
    date = models.DateField(default = datetime.date.today, validators = [MinValueValidator(datetime.date.today)])
    trailer_type = models.CharField(max_length = 64, choices = TrailerType.choices)
    tanker_volume = models.ForeignKey(TankerTrailer, on_delete = models.CASCADE, blank = True, null = True, related_name = "transportation_order")
    load_weight = models.PositiveSmallIntegerField(validators = [MinValueValidator(0), MaxValueValidator(24000)])
    load_place = models.ForeignKey(LoadOrDeliveryPlace, on_delete = models.PROTECT, related_name = "transportation_order_load")
    delivery_place = models.ForeignKey(LoadOrDeliveryPlace, on_delete = models.PROTECT, related_name = "transportation_order_delivery")
    driver = models.OneToOneField(CustomUser, limit_choices_to = {"role": "Driver"}, on_delete = models.SET_NULL,
                               related_name = "assigned_order", null = True, blank = True)
    done = models.BooleanField(default = False, null = True, blank = True)

    objects = models.Manager()
    current = CurrentOrderManager()
    archived = ArchivedOrderManager()

    def place_restrict(self):
        load_place_id = self.load_place_id
        delivery_place_id = self.delivery_place_id
        if load_place_id == delivery_place_id:
            raise Exception("Load place cannot be the same as delivery place.")

    def empty_tanker_volume(self):
        if self.trailer_type == "Tanker trailer" and self.tanker_volume == None:
            raise Exception("Order for tanker trailer must have tanker chamber volumes set up.")

    def __str__(self):
        if self.trailer_type == "Tanker trailer":
            return f"TRANSPORTATION ORDER DATE: {self.date}, LOAD PLACE: {self.load_place}, TRAILER: {self.trailer_type}," \
                   f" TANKER VOLUME: {self.tanker_volume}, WEIGHT: {self.load_weight}, DELIVERY PLACE: {self.delivery_place}, DONE: {self.done}"
        else:
            return f"TRANSPORTATION ORDER DATE: {self.date}, LOAD PLACE: {self.load_place}, TRAILER: {self.trailer_type}," \
                   f" WEIGHT: {self.load_weight}, DELIVERY PLACE: {self.delivery_place}, DONE: {self.done}"





