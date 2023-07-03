from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class TrailerType(models.TextChoices):
        CURTAIN_SIDE = "Curtain-side trailer"
        REFRIGERATED = "Refrigerated trailer"
        TIPPER = "Tipper trailer"
        LOW_LOADER = "Low-loader trailer"
        CONTAINER = "Container trailer"
        SELF_UNLOADING = "Self-unloading trailer"
        TANKER = "Tanker trailer"
        INSULATED = "Insulated trailer"

class LoadPlace(models.Model):
    country = models.CharField(max_length = 64)
    state = models.CharField(max_length = 64)
    town = models.CharField(max_length = 64)
    postal_code = models.CharField(max_length = 16)
    street = models.CharField(max_length = 64)
    street_number = models.PositiveSmallIntegerField()
    contact_number = models.PositiveSmallIntegerField(blank = True, null = True)

    def __str__(self):
        return f"Load place: {self.country} - {self.state} - {self.town} {self.postal_code}, st. {self.street} {self.street_number}, Contact: {self.contact_number}"

class TransportationOrder(models.Model):
    date = models.DateField(default = datetime.date.today, validators = [MinValueValidator(datetime.date.today)])
    trailer_type = models.CharField(max_length = 64, choices = TrailerType.choices)
    load_weight = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(24)])
    load_place = models.ForeignKey(LoadPlace, on_delete = models.PROTECT, related_name = "transportation_order")

class Delivery(models.Model):
    country = models.CharField(max_length = 64)
    state = models.CharField(max_length = 64)
    town = models.CharField(max_length = 64)
    postal_code = models.CharField(max_length = 16)
    street = models.CharField(max_length = 64)
    street_number = models.PositiveSmallIntegerField()
    contact_number = models.PositiveSmallIntegerField(blank = True, null = True)
    cargo_weight = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(24)], default = 'Whole cargo')
    transportation_order = models.ForeignKey(TransportationOrder, on_delete = models.PROTECT, related_name = "delivery")

    def __str__(self):
        return f"Delivery place: {self.country} - {self.state} - {self.town} {self.postal_code}, st. {self.street} {self.street_number}, Contact: {self.contact_number}, Cargo weight: {self.cargo_weight}t."



