from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TransportationOrder, LoadPlace, Delivery

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class TransportationOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransportationOrder
        fields = ['id', 'trailer_type', 'load_weight', 'load_place', 'delivery']

class LoadPlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoadPlace
        fields = ['id', 'country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number']

class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number', 'cargo_weight']


