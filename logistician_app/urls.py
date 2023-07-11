from django.urls import path
from logistician_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html')),

    path('orders_list/', views.TransportationOrderListView.as_view(), name = 'orders-list'),
    path('order/<int:pk>/', views.TransportationOrderRetrieveView.as_view(), name = 'order-retrieve'),
    path('order_create/', views.TransportationOrderCreateView.as_view(), name = 'order-create'),
    path('order_update/<int:pk>/', views.TransportationOrderUpdateView.as_view(), name = 'order-update'),
    path('order_destroy/<int:pk>/', views.TransportationOrderDestroyView.as_view(), name = 'order-destroy')
]
