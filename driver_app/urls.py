from django.urls import path
from driver_app import views

urlpatterns = [
    path('your_order/', views.CurrentOrder.as_view(), name = 'current-order')
]
