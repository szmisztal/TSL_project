from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer

class TransportationOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TransportationOrderSerializer

    def get_queryset(self):
        orders = TransportationOrder.objects.all().order_by("id")
        return orders

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = TransportationOrderSerializer(order)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = TransportationOrder.objects.create(date = request.data["date"],
                                                   trailer_type = request.data["trailer_type"],
                                                   tanker_volume = request.data["tanker_volume"],
                                                   load_weight = request.data["load_weight"],
                                                   load_place = request.data["load_place"],
                                                   delivery_place = request.datap["delivery_place"])
        serializer = TransportationOrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order.date = request.data["date"]
        order.trailer_type = request.data["trailer_type"]
        order.tanker_volume = request.data["tanker_volume"]
        order.load_weight = request.data["load_weight"]
        order.load_place = request.data["load_place"]
        order.delivery_place = request.data["delivery_place"]
        order.save()
        serializer =TransportationOrderSerializer(order)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response("Order deleted")

class LoadOrDeliveryPlaceViewSet(viewsets.ModelViewSet):
    queryset = LoadOrDeliveryPlace.objects.all()
    serializer_class = LoadOrDeliveryPlaceSerializer

class TankerTrailerViewSet(viewsets.ModelViewSet):
    queryset = TankerTrailer.objects.all()
    serializer_class = TankerTrailerSerializer
