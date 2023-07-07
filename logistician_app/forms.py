from django import forms
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer

class OrderForm(forms.ModelForm):
    class Meta:
        model = TransportationOrder
        fields = ['date', 'trailer_type', 'load_place', 'tanker_volume', 'load_weight', 'delivery_place']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = LoadOrDeliveryPlace
        fields = ['country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number']

class TankerTrailerForm(forms.ModelForm):
    class Meta:
        model = TankerTrailer
        fields = ['chamber_1', 'chamber_2', 'chamber_3', 'chamber_4', 'chamber_5']
