from django.shortcuts import render
from django.views import generic
from user_app.permissions import IsLogistician, IsDispatcher, IsDriver

class HomepageView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        context = {
            "is_logistician": IsLogistician().has_permission(request, None),
            "is_dispatcher": IsDispatcher().has_permission(request, None),
            "is_driver": IsDriver().has_permission(request, None)
        }
        return render(request, "index.html", context)
