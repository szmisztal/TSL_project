from django.shortcuts import render
from rest_framework import viewsets
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer

class TransportationOrderViewSet(viewsets.ModelViewSet):
    queryset = TransportationOrder.objects.all()
    serializer_class = TransportationOrderSerializer

class LoadOrDeliveryPlaceViewSet(viewsets.ModelViewSet):
    queryset = LoadOrDeliveryPlace.objects.all()
    serializer_class = LoadOrDeliveryPlaceSerializer

class TankerTrailerViewSet(viewsets.ModelViewSet):
    queryset = TankerTrailer.objects.all()
    serializer_class = TankerTrailerSerializer
