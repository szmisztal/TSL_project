from django.urls import path
from dispatcher_app import views

urlpatterns = [
    path('assign_order/', views.OrdersListView.as_view(), name = 'assign-order'),
     path('make_assign/<int:pk>/', views.assign_order_to_driver, name = 'make-assign'),
]
