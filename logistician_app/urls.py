from django.urls import path
from logistician_app import views

urlpatterns = [
    path('orders_list/', views.TransportationOrderView.as_view(), name = 'orders-list'),
    path('order/<int:pk>/', views.TransportationOrderView.as_view(), name = 'order-retrieve'),
    path('order_create/', views.TransportationOrderCreateOrUpdateView.as_view(), name = 'order-create'),
    path('order_update/<int:pk>/', views.TransportationOrderCreateOrUpdateView.as_view(), name = 'order-update'),
    path('order_destroy/<int:pk>/', views.TransportationOrderDestroyView.as_view(), name = 'order-destroy'),
    path('archived_orders_list', views.ArchivedTransportationOrderView.as_view(), name = 'archived-orders'),

    path('places_list/', views.PlaceView.as_view(), name = 'places-list'),
    path('place/<int:pk>/', views.PlaceView.as_view(), name = 'place-retrieve'),
    path('place_create/', views.PlaceCreateOrUpdateView.as_view(), name = 'place-create'),
    path('place_update/<int:pk>/', views.PlaceCreateOrUpdateView.as_view(), name = 'place-update'),
    path('place_destroy/<int:pk>/', views.PlaceDestroyView.as_view(), name = 'place-destroy'),

    path('tanker_create/', views.TankerCreateOrUpdateView.as_view(), name = 'tanker-create'),
    path('tanker_update/<int:pk>/', views.TankerCreateOrUpdateView.as_view(), name = 'tanker-update'),
]




