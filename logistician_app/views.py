from django.shortcuts import render
from rest_framework import viewsets
from .models import TransportationOrder, LoadPlace, Delivery
from .serializers import TransportationOrderSerializer, LoadPlaceSerializer, DeliverySerializer

class TransportationOrderViewSet(viewsets.ModelViewSet):
    queryset = TransportationOrder.objects.all()
    serializer_class = TransportationOrderSerializer

class LoadPlaceViewSet(viewsets.ModelViewSet):
    queryset = LoadPlace.objects.all()
    serializer_class = LoadPlaceSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
