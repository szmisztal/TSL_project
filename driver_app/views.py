from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from user_app.permissions import IsDriver
from user_app.models import CustomUser
from logistician_app.models import TransportationOrder
from .forms import OrderDoneForm

@method_decorator(login_required, name = "dispatch")
@permission_classes([IsDriver])
class CurrentOrder(APIView):
    form_class = OrderDoneForm
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "driver_order_form.html"

    def get(self, request, *args, **kwargs):
        try:
            driver = request.user
            order = TransportationOrder.objects.get(driver_id = driver)
        except TransportationOrder.DoesNotExist:
            messages.error(request, "You don`t have any order right now. Try later.")
            return render(request, "index.html")
        return Response({"form": self.form_class, "order": order}, template_name = self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            driver = request.user
            order = TransportationOrder.objects.get(driver_id = driver)
        except TransportationOrder.DoesNotExist:
            messages.error(request, "You don`t have any order right now. Try later.")
            return render(request, "index.html")
        form = self.form_class(request.POST)
        if form.is_valid():
            done = form.cleaned_data["done"]
            order.done = done
            order.driver = None
            order.save()
            messages.success(request, "Order finished")
            try:
                send_emails(request)
            except Exception as e:
                messages.error(request, f"Failed to send emails: {e}")
            return redirect("homepage")
        else:
            form = self.form_class()
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
        f"{driver.first_name} {driver.last_name} has finished his order.",
        "sz.misztal@gmail.com",
        emails,
        fail_silently = False
    )



