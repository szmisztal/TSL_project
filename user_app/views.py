from rest_framework import viewsets
from django.views import generic
from .serializers import UserSerializer
from .models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("id")
    serializer_class = UserSerializer

class HomepageView(generic.TemplateView):
    template_name = "index.html"

