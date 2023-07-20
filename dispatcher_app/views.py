from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from logistician_app.serializers import TransportationOrderSerializer
from logistician_app.models import TransportationOrder
from .forms import AssignForm

@login_required
@transaction.atomic
def assign_order_to_driver(request):
    if request.method == "POST":
        form = AssignForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data["driver"]
            order = form.cleaned_data["order"]
            try:
                order.driver = driver
                order.save()
                return redirect("assign-orders-list")
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = AssignForm()
    return render(request, "assign_order_to_driver.html", {"form": form})

@method_decorator(login_required, name = "dispatch")
class AssignedOrdersView(ListAPIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "assigned_orders_list.html"

    def get(self, request, *args, **kwargs):
        orders = TransportationOrder.objects.all().order_by("driver")
        return Response({"serializer": self.serializer_class(orders), "orders": orders},
                        template_name = self.template_name)


