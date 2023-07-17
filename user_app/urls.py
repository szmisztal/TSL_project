from django.urls import path
from django.views.generic import TemplateView
from .views import sign_in, sign_out, sign_up

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    path('register/', sign_up, name = 'register'),
    path('login/', sign_in, name = 'login'),
    path('logout/', sign_out, name = 'logout')
]
