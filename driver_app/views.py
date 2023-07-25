from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from rest_framework.decorators import permission_classes
from user_app.permissions import IsDriver
from user_app.models import CustomUser
from logistician_app.models import TransportationOrder
from .forms import OrderDoneForm

@login_required
@permission_classes([IsDriver])
def current_order(request):
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
            order.driver = None
            order.save()
            messages.success(request, "Order finished")
            send_emails(request)
            return redirect("homepage")
    else:
        form = OrderDoneForm()
    return render(request, "driver_order_form.html", {"form": form, "order": order})

def send_emails(request):
    emails = []
    driver = request.user
    dispatchers = CustomUser.objects.filter(role = "Dispatcher")
    for user in dispatchers:
        email = user.email
        emails.append(email)

    send_mail(
        "ORDER FINISHED",
        f"{driver.first_name} {driver.last_name} finished his order.",
        "app.mail@gmail.com",
        emails + ["sz.misztal@gmail.com"],
        fail_silently=False
    )



