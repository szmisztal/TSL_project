from django.urls import path
from django.views.generic import TemplateView
from dispatcher_app import views

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    path('assign_order/', views.assign_order_to_driver, name = "assign-order"),
    path('assign_orders_list/', views.AssignedOrdersView.as_view(), name = "assigned-orders-list")
]
