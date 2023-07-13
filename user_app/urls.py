from django.urls import path
from django.views.generic import TemplateView
from user_app import views

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    # path('register/')
]
