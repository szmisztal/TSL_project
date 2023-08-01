from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from user_app.permissions import IsLogistician
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer
from .forms import OrderForm, PlaceForm, TankerForm

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderView(APIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        orders = TransportationOrder.objects.all().order_by("done", "date")
        order_id = kwargs.get("pk")
        if order_id:
            order = get_object_or_404(TransportationOrder, id = order_id)
            return Response({"serializer": self.serializer_class(order), "order": order},
                            template_name = "order_retrieve.html")
        else:
            return Response({"serializer": self.serializer_class(orders), "orders": orders},
                        template_name = "orders_list.html")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderCreateOrUpdateView(APIView):
    serializer_class = TransportationOrderSerializer
    form_class = OrderForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_form.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        if order_id:
            order = get_object_or_404(TransportationOrder, id = order_id)
            tanker = order.tanker_volume
            form = self.form_class(instance = order)
            return Response({"serializer": self.serializer_class(order), "form": form, "order": order, "tanker": tanker},
                            template_name = self.template_name)
        else:
            form = self.form_class()
            return Response({"form": form}, template_name = self.template_name)

    def validate_and_save_order(self, order, form):
        try:
            order.place_restrict()
            order.empty_tanker_volume()
        except Exception as e:
            messages.error(self.request, str(e))
            form.initial = form.cleaned_data
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
        try:
            order.full_clean()
        except Exception as e:
            messages.error(self.request, str(e))
            form.initial = form.cleaned_data
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
        order.save()
        return None

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        form = self.form_class(request.POST)
        tanker = None
        if order_id:
            order = get_object_or_404(TransportationOrder, id = order_id)
            form = self.form_class(request.POST, instance = order)
            tanker = order.tanker_volume
        if form.is_valid():
            order = form.save(commit = False)
            response = self.validate_and_save_order(order, form)
            if response is not None:
                return response
            if order_id:
                messages.success(self.request, "Transportation order updated successfully.")
                return redirect("orders-list")
            else:
                messages.success(self.request, "Transportation order created successfully.")
                return redirect("orders-list")
        return Response({"form": form, "tanker": tanker}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderDestroyView(APIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_delete.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        return Response({"serializer": self.serializer_class(order), "order": order},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        tanker = order.tanker_volume
        order.delete()
        if tanker:
            tanker.delete()
        messages.success(self.request, "Transportation order deleted successfully.")
        return redirect("orders-list")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceView(APIView):
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        places = LoadOrDeliveryPlace.objects.all().order_by("country")
        place_id = kwargs.get("pk")
        if place_id:
            place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
            return Response({"serializer": self.serializer_class(place), "place": place},
                        template_name = "place_retrieve.html")
        else:
            return Response({"serializer": self.serializer_class(places), "places": places},
                        template_name = "places_list.html")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceCreateOrUpdateView(APIView):
    serializer_class = LoadOrDeliveryPlaceSerializer
    form_class = PlaceForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_form.html"

    def get(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        if place_id:
            place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
            form = self.form_class(instance = place)
            return Response({"serializer": self.serializer_class(place), "form": form, "place": place},
                        template_name = self.template_name)
        else:
            form = self.form_class()
            return Response({"form": form}, template_name = self.template_name)

    def save_place(self, form, place = None):
        if form.is_valid():
            if place is None:
                place = form.save()
                success_message = "Place created successfully."
            else:
                place = form.save()
                success_message = "Place updated successfully."
            messages.success(self.request, success_message)
            return place
        return None

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        form = self.form_class(request.POST)
        if place_id:
            place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
            form = self.form_class(request.POST, instance = place)
        else:
            place = None
        saved_place = self.save_place(form, place)
        if saved_place:
            return redirect("places-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceDestroyView(APIView):
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_delete.html"

    def get(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
        return Response({"serializer": self.serializer_class(place), "place": place},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
        try:
            place.delete()
            messages.success(self.request, "Place deleted successfully.")
            return redirect("places-list")
        except Exception as e:
            messages.error(self.request, "This place belongs to some transportation order.")
            return redirect("places-list")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerCreateOrUpdateView(APIView):
    serializer_class = TankerTrailerSerializer
    form_class = TankerForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tanker_form.html"

    def get(self, request, *args, **kwargs):
        tanker_id = kwargs.get("pk")
        if tanker_id:
            tanker = get_object_or_404(TankerTrailer, id = tanker_id)
            form = self.form_class(instance = tanker)
            return Response({"serializer": self.serializer_class(tanker), "form": form, "tanker": tanker},
                        template_name = self.template_name)
        else:
            form = self.form_class()
            return Response({"form": form}, template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tanker_id = kwargs.get("pk")
        if tanker_id:
            tanker = get_object_or_404(TankerTrailer, id = tanker_id)
            form = self.form_class(request.POST, instance = tanker)
            if form.is_valid():
                form.save()
                messages.success(self.request, "Tanker trailer volumes updated successfully.")
                return redirect("orders-list")
            else:
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(self.request, "Tanker trailer volumes set up successfully.")
                return redirect("order-create")
            else:
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

