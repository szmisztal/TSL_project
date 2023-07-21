from django import forms
from user_app.models import CustomUser
from logistician_app.models import TransportationOrder

class AssignForm(forms.ModelForm):
    driver = forms.ModelChoiceField(queryset = CustomUser.drivers.all(), empty_label = "-------", required = False)

    class Meta:
        model = TransportationOrder
        fields = ["driver"]
