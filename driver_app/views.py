from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import permission_classes
from user_app.permissions import IsDriver
from logistician_app.models import TransportationOrder
from .forms import OrderDoneForm

@login_required
@permission_classes([IsDriver])
def actual_order(request):
    try:
        driver = request.user
        order = TransportationOrder.objects.get(driver_id = driver)
    except TransportationOrder.DoesNotExist as e:
        messages.error(request, str(e))
        return render(request, "index.html")
    if request.method == "POST":
        form = OrderDoneForm(request.POST)
        if form.is_valid():
            done = form.cleaned_data["done"]
            order.done = done
            order.save()
            messages.success(request, "Order finished")
            return redirect("homepage")
    else:
        form = OrderDoneForm()
    return render(request, "driver_order_form.html", {"form": form, "order": order})
