from django import forms
from .models import TransportationOrder

class OrderForm(forms.ModelForm):
    class Meta:
        model = TransportationOrder
        fields = ['date', 'trailer_type', 'load_place', 'tanker_volume', 'load_weight', 'delivery_place']
