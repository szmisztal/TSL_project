from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'transportation_orders', views.TransportationOrderViewSet, basename = 'transportation_order')
router.register(r'load_places', views.LoadPlaceViewSet, basename = 'load_place')
router.register(r'delivery', views.DeliveryViewSet, basename = 'delivery')

url_patterns = [
    path('', include(router.urls))
]
