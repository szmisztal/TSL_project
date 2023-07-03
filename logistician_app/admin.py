from django.contrib import admin
from .models import TransportationOrder, LoadPlace, Delivery

admin.site.register(TransportationOrder)
admin.site.register(LoadPlace)
admin.site.register(Delivery)
