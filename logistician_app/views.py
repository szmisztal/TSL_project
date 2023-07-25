from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from user_app.permissions import IsLogistician
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer
from .forms import OrderForm, PlaceForm, TankerForm

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderListView(ListAPIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "orders_list.html"

    def get(self, request, *args, **kwargs):
        orders = TransportationOrder.objects.all().order_by("id")
        return Response({"serializer": self.serializer_class(orders), "orders": orders},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderRetrieveView(RetrieveAPIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_retrieve.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        return Response({"serializer": self.serializer_class(order), "order": order},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderCreateView(CreateAPIView):
    form_class = OrderForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_form.html"

    def get(self, request):
        form = self.form_class()
        return Response({"form": form}, template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        next_url = request.GET.get("next")
        if form.is_valid():
            order = form.save(commit = False)
            load_place_id = order.load_place_id
            delivery_place_id = order.delivery_place_id
            try:
                order.place_restrict(load_place_id = load_place_id, delivery_place_id = delivery_place_id)
                order.empty_tanker_volume()
            except ValueError as e:
                messages.error(self.request, str(e))
                form.initial = form.cleaned_data
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
            try:
                order.full_clean()
            except ValidationError as e:
                messages.error(self.request, str(e))
                form.initial = form.cleaned_data
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
            order.save()
            messages.success(self.request, "Transportation order created successfully.")
            if next_url:
                redirect(next_url)
            else:
                return redirect("orders-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderUpdateView(UpdateAPIView):
    queryset = TransportationOrder.objects.all()
    serializer_class = TransportationOrderSerializer
    form_class = OrderForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_form.html"

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        form = self.form_class(instance = order)
        return Response({"serializer": self.serializer_class(order), "form": form, "order": order},
                        template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        form = self.form_class(request.POST, instance = order)
        next_url = request.Get.get("next")
        if form.is_valid():
            order = form.save(commit = False)
            load_place_id = order.load_place_id
            delivery_place_id = order.delivery_place_id
            try:
                order.place_restrict(load_place_id = load_place_id, delivery_place_id = delivery_place_id)
                order.empty_tanker_volume()
            except ValueError as e:
                messages.error(self.request, str(e))
                form.initial = form.cleaned_data
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
            try:
                order.full_clean()
            except ValidationError as e:
                messages.error(self.request, str(e))
                form.initial = form.cleaned_data
                return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
            order.save()
            messages.success(self.request, "Transportation order updated successfully.")
            if next_url:
                redirect(next_url)
            else:
                return redirect("orders-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TransportationOrderDestroyView(DestroyAPIView):
    queryset = TransportationOrder.objects.all()
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_delete.html"

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        return Response({"serializer": self.serializer_class(order), "order": order},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        tanker = order.tanker_volume
        order.delete()
        if tanker:
            tanker.delete()
        messages.success(self.request, "Transportation order deleted successfully.")
        return redirect("orders-list")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceListView(ListAPIView):
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "places_list.html"

    def get(self, request, *args, **kwargs):
        places = LoadOrDeliveryPlace.objects.all().order_by("country")
        return Response({"serializer": self.serializer_class(places), "places": places},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceRetrieveView(RetrieveAPIView):
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_retrieve.html"

    def get(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        place = get_object_or_404(LoadOrDeliveryPlace, id = place_id)
        return Response({"serializer": self.serializer_class(place), "place": place},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceCreateView(CreateAPIView):
    form_class = PlaceForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_form.html"

    def get(self, request):
        form = self.form_class()
        return Response({"form": form}, template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Place created successfully.")
            return redirect("places-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceUpdateView(UpdateAPIView):
    queryset = LoadOrDeliveryPlace.objects.all()
    serializer_class = LoadOrDeliveryPlaceSerializer
    form_class = PlaceForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_form.html"

    def get(self, request, *args, **kwargs):
        place = self.get_object()
        form = self.form_class(instance = place)
        return Response({"serializer": self.serializer_class(place), "form": form, "place": place},
                        template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        place = self.get_object()
        form = self.form_class(request.POST, instance = place)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Place updated successfully.")
            return redirect("places-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class PlaceDestroyView(DestroyAPIView):
    queryset = LoadOrDeliveryPlace.objects.all()
    serializer_class = LoadOrDeliveryPlaceSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "place_delete.html"

    def get(self, request, *args, **kwargs):
        place = self.get_object()
        return Response({"serializer": self.serializer_class(place), "place": place},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        place = self.get_object()
        place.delete()
        messages.success(self.request, "Place deleted successfully.")
        return redirect("places-list")

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerListView(ListAPIView):
    serializer_class = TankerTrailerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tankers_list.html"

    def get(self, request, *args, **kwargs):
        tankers = TankerTrailer.objects.all().order_by("id")
        return Response({"serializer": self.serializer_class(tankers), "tankers": tankers},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerRetrieveView(RetrieveAPIView):
    serializer_class = TankerTrailerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tanker_retrieve.html"

    def get(self, request, *args, **kwargs):
        tanker_id = kwargs.get("pk")
        tanker = get_object_or_404(TankerTrailer, id = tanker_id)
        return Response({"serializer": self.serializer_class(tanker), "tanker": tanker},
                        template_name = self.template_name)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerCreateView(CreateAPIView):
    form_class = TankerForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tanker_form.html"

    def get(self, request):
        form = self.form_class()
        return Response({"form": form}, template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Tanker trailer volumes set up successfully.")
            return redirect("order-create")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerUpdateView(UpdateAPIView):
    queryset = TankerTrailer.objects.all()
    serializer_class = TankerTrailerSerializer
    form_class = TankerForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tanker_form.html"

    def get(self, request, *args, **kwargs):
        tanker = self.get_object()
        form = self.form_class(instance = tanker)
        return Response({"serializer": self.serializer_class(tanker), "form": form, "tanker": tanker},
                        template_name = self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        tanker = self.get_object()
        form = self.form_class(request.POST, instance = tanker)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Tanker trailer volumes updated successfully.")
            return redirect("orders-list")
        else:
            return Response({"form": form}, template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsLogistician])
class TankerDestroyView(DestroyAPIView):
    queryset = TankerTrailer.objects.all()
    serializer_class = TankerTrailerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tanker_delete.html"

    def get(self, request, *args, **kwargs):
        tanker = self.get_object()
        return Response({"serializer": self.serializer_class(tanker), "tanker": tanker},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        tanker = self.get_object()
        tanker.delete()
        messages.success(self.request, "Tanker trailer object deleted successfully.")
        return redirect("homepage")
