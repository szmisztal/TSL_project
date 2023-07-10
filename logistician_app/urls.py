from django.urls import path
from logistician_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html')),
    path('all_orders/', views.TransportationOrderViewSet.as_view(), name = 'orders-list'),
    path('order/<int:pk>', views.TransportationOrderViewSet.as_view(), name = 'transportation_order-detail'),
]
