from django.urls import path
from driver_app import views

urlpatterns = [
    path('your_order/', views.actual_order, name = 'actual-order')
]
