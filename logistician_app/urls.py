from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from logistician_app import views

router = routers.DefaultRouter()
router.register(r'transportation_orders', views.TransportationOrderViewSet)
router.register(r'load_places', views.LoadPlaceViewSet)
router.register(r'deliveries', views.DeliveryViewSet)

url_patterns = [
    path('', include(router.urls))
]
