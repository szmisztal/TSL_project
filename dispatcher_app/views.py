from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from user_app.permissions import IsDispatcher
from logistician_app.serializers import TransportationOrderSerializer
from logistician_app.models import TransportationOrder
from .forms import AssignForm

@login_required
@permission_classes([IsDispatcher])
@transaction.atomic
def assign_order_to_driver(request, pk):
    try:
        order = TransportationOrder.current.get(pk = pk)
    except TransportationOrder.DoesNotExist as e:
        messages.error(request, str(e))
        return redirect("assign-order")

    if request.method == "POST":
        form = AssignForm(request.POST)
        if form.is_valid():
            driver = form.cleaned_data["driver"]
            order.driver = driver
            order.save()
            messages.success(request, "Assign done.")
            return redirect("assign-order")
    else:
        form = AssignForm()

    return render(request, "assign_order_form.html", {"form": form, "order": order})

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsDispatcher])
class OrdersListView(APIView):
    serializer_class = TransportationOrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "assign_order.html"

    def get(self, request, *args, **kwargs):
        orders = TransportationOrder.current.all().order_by("date")
        return Response({"serializer": self.serializer_class(orders), "orders": orders},
                        template_name = self.template_name)


