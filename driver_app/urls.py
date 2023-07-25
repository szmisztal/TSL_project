from django.urls import path
from driver_app import views

urlpatterns = [
    path('your_order/', views.current_order, name = 'current-order')
]
