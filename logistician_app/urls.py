from django.urls import path
from logistician_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),

    path('orders_list/', views.TransportationOrderListView.as_view(), name = 'orders-list'),
    path('order/<int:pk>/', views.TransportationOrderRetrieveView.as_view(), name = 'order-retrieve'),
    path('order_create/', views.TransportationOrderCreateView.as_view(), name = 'order-create'),
    path('order_update/<int:pk>/', views.TransportationOrderUpdateView.as_view(), name = 'order-update'),
    path('order_destroy/<int:pk>/', views.TransportationOrderDestroyView.as_view(), name = 'order-destroy'),

    path('places_list/', views.PlaceListView.as_view(), name = 'places-list'),
    path('place/<int:pk>/', views.PlaceRetrieveView.as_view(), name = 'place-retrieve'),
    path('place_create/', views.PlaceCreateView.as_view(), name = 'place-create'),
    path('place_update/<int:pk>/', views.PlaceUpdateView.as_view(), name = 'place-update'),
    path('place_destroy/<int:pk>/', views.PlaceDestroyView.as_view(), name = 'place-destroy'),

    path('tankers_list/', views.TankerListView.as_view(), name = 'tankers-list'),
    path('tanker/<int:pk>/', views.TankerRetrieveView.as_view(), name = 'tanker-retrieve'),
    path('tanker_create/', views.TankerCreateView.as_view(), name = 'tanker-create'),
    path('tanker_update/<int:pk>/', views.TankerUpdateView.as_view(), name = 'tanker-update'),
    path('tanker_destroy/<int:pk>/', views.TankerDestroyView.as_view(), name = 'tanker-destroy')
]





