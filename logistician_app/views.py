from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import TransportationOrder, LoadOrDeliveryPlace, TankerTrailer
from .serializers import TransportationOrderSerializer, LoadOrDeliveryPlaceSerializer, TankerTrailerSerializer
from .forms import OrderForm

class TransportationOrderListView(ListAPIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "orders_list.html"

    def list(self, request, *args, **kwargs):
        orders = TransportationOrder.objects.all().order_by("id")
        return Response({"serializer": self.serializer_class(orders), "orders": orders},
                        template_name = self.template_name)

class TransportationOrderRetrieveView(RetrieveAPIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_retrieve.html"

    def retrieve(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        return Response({"serializer": self.serializer_class(order), "order": order},
                        template_name = self.template_name)

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
        if form.is_valid():
            order = form.save()
            return redirect('order-retrieve', pk = order.pk)
        return Response({"form": form}, template_name = self.template_name)

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
        if form.is_valid():
            form.save()
            return redirect("orders-list")
        else:
            return Response({"serializer": self.serializer_class(order), "form": form, "order": order},
                            template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)

class TransportationOrderDestroyView(DestroyAPIView):
    queryset = TransportationOrder.objects.all()
    serializer_class = TransportationOrderSerializer
    form_class = OrderForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "order_delete.html"

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        form = self.form_class(instance = order)
        return Response({"serializer": self.serializer_class(order), "form": form, "order": order},
                        template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        form = self.form_class(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect("orders-list")
        else:
            return Response({"serializer": self.serializer_class(order), "form": form, "order": order},
                            template_name = self.template_name, status = status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")
        order = get_object_or_404(TransportationOrder, id = order_id)
        self.perform_destroy(order)
        return Response(status = status.HTTP_204_NO_CONTENT)



