from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer

class TransportationOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        orders = TransportationOrder.objects.all()
        return orders

    def list(self, request):
        orders = TransportationOrder.objects.all().order_by("id")
        template_name = "all_orders.html"
        return Response({"orders": orders}, template_name = template_name)

    def retrieve(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        serializer = TransportationOrderSerializer(order)
        template_name = "order_detail.html"
        return Response({"serializer": serializer, "order": order}, template_name = template_name)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = TransportationOrder.objects.create(date = request.data["date"],
                                                   trailer_type = request.data["trailer_type"],
                                                   tanker_volume = request.data["tanker_volume"],
                                                   load_weight = request.data["load_weight"],
                                                   load_place = request.data["load_place"],
                                                   delivery_place = request.data["delivery_place"])
        serializer = TransportationOrderSerializer(order)
        return Response(serializer.data, template_name = "create_order")

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
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        places = LoadOrDeliveryPlace.objects.all()
        return places

    def list(self, request, *args, **kwargs):
        places = LoadOrDeliveryPlace.objects.all().order_by("id")
        template_name = "all_places.html"
        return Response({"places": places}, template_name = template_name)

    def retrieve(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
        serializer = LoadOrDeliveryPlaceSerializer(place)
        template_name = "place_detail.html"
        return Response({"serializer": serializer, "place": place}, template_name = template_name)

class TankerTrailerViewSet(viewsets.ModelViewSet):
    serializer_class = TankerTrailerSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        tankers = TankerTrailer.objects.all()
        return tankers

    def list(self, request, *args, **kwargs):
        tankers = TankerTrailer.objects.all().order_by("id")
        template_name = "all_tankers.html"
        return Response({"tankers": tankers}, template_name = template_name)

    def retrieve(self, request, *args, **kwargs):
        tanker_id = kwargs.get("pk")
        tanker = get_object_or_404(TankerTrailer, id = tanker_id)
        serializer = TankerTrailerSerializer(tanker)
        template_name = "tanker_detail.html"
        return Response({"serializer": serializer, "tanker": tanker}, template_name = template_name)

