from rest_framework import serializers
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer

class LoadOrDeliveryPlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoadOrDeliveryPlace
        fields = ['id', 'country', 'state', 'town', 'postal_code', 'street', 'street_number', 'contact_number']

class TankerTrailerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TankerTrailer
        fields = ['chamber_1', 'chamber_2', 'chamber_3', 'chamber_4', 'chamber_5']

class TransportationOrderSerializer(serializers.HyperlinkedModelSerializer):
    load_place = LoadOrDeliveryPlaceSerializer(many = False)
    delivery_place = LoadOrDeliveryPlaceSerializer(many = False)
    tanker_volume = TankerTrailerSerializer(many = False)

    class Meta:
        model = TransportationOrder
        fields = ['id', 'date', 'trailer_type', 'load_place', 'tanker_volume', 'load_weight', 'delivery_place']






