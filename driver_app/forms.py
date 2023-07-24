from django import forms
from logistician_app.models import TransportationOrder

class OrderDoneForm(forms.ModelForm):
    done = forms.BooleanField

    class Meta:
        model = TransportationOrder
        fields = ["done"]
