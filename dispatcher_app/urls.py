from django.urls import path
from dispatcher_app import views

urlpatterns = [
    path('assign_order/', views.assign_order_to_driver, name = 'assign-order'),
    path('assign_update/<int:pk>/', views.assign_order_to_driver, name = 'assign-update'),
    path('assign_orders_list/', views.AssignedOrdersView.as_view(), name = 'assigned-orders-list')
]
