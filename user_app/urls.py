from django.urls import path
from django.views.generic import TemplateView
from .views import sign_in, sign_out

urlpatterns = [
    path('login/', sign_in, name = 'login'),
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    path('logout/', sign_out, name = 'logout')
]
