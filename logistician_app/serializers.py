from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TransportationOrder, LoadPlace, Delivery

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class LoadPlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoadPlace
        fields = ['country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number']

class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ['country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number', 'cargo_weight']

class TransportationOrderSerializer(serializers.HyperlinkedModelSerializer):
    load_place = LoadPlaceSerializer(many = False)
    delivery = DeliverySerializer(many = True)
    class Meta:
        model = TransportationOrder
        fields = ['date', 'trailer_type', 'load_place', 'load_weight', 'delivery']


