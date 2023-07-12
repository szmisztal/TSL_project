from django import forms
from .models import TransportationOrder, LoadOrDeliveryPlace

class OrderForm(forms.ModelForm):
    class Meta:
        model = TransportationOrder
        fields = ['date', 'trailer_type', 'load_place', 'tanker_volume', 'load_weight', 'delivery_place']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = LoadOrDeliveryPlace
        fields = ['company', 'country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number']
