from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

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
    company = models.CharField(max_length = 64)
    country = models.CharField(max_length = 64)
    state = models.CharField(max_length = 64)
    town = models.CharField(max_length = 64)
    postal_code = models.CharField(max_length = 16)
    street = models.CharField(max_length = 64)
    street_number = models.PositiveSmallIntegerField()
    contact_number = models.PositiveSmallIntegerField(blank = True, null = True)

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
        whole_volume = self.chamber_1 + self.chamber_2 + self.chamber_3 + self.chamber_4 + self.chamber_5
        return whole_volume

    def __str__(self):
        return str(self.get_volume())

class TransportationOrder(models.Model):
    date = models.DateField(default = datetime.date.today, validators = [MinValueValidator(datetime.date.today)])
    trailer_type = models.CharField(max_length = 64, choices = TrailerType.choices)
    tanker_volume = models.OneToOneField(TankerTrailer, on_delete = models.CASCADE, blank = True, null = True, related_name = "tanker+")
    load_weight = models.PositiveSmallIntegerField(validators = [MinValueValidator(0), MaxValueValidator(24000)])
    load_place = models.ForeignKey(LoadOrDeliveryPlace, on_delete = models.PROTECT, related_name = "transportation order load+")
    delivery_place = models.ForeignKey(LoadOrDeliveryPlace, on_delete = models.PROTECT, related_name = "transportation order delivery+")

    def __str__(self):
        if self.trailer_type == "Tanker trailer":
            return f"Transportation order date: {self.date}, \nLoad place: {self.load_place} \nTanker volume: {self.tanker_volume}. " \
                   f"\nDelivery place: {self.delivery_place}"
        else:
            return f"Transportation order date: {self.date}, \nLoad place: {self.load_place} \nTrailer: {self.trailer_type}. " \
                   f"\nWeight: {self.load_weight}. \nDelivery place: {self.delivery_place}"





