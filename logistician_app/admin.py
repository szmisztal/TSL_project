from django.contrib import admin
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer

admin.site.register(TransportationOrder)
admin.site.register(LoadOrDeliveryPlace)
admin.site.register(TankerTrailer)

