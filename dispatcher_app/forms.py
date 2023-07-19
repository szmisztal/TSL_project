from django import forms
from user_app.models import CustomUser
from logistician_app.models import TransportationOrder

class AssignForm(forms.Form):
    driver = forms.ModelChoiceField(queryset = CustomUser.drivers.all(), empty_label = "Select a driver")
    order = forms.ModelChoiceField(queryset = TransportationOrder.unassigned_orders.all(), empty_label = "Select a order")


