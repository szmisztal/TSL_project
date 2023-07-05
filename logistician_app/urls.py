from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from logistician_app import views

router = routers.DefaultRouter()
router.register(r'transportation_orders', views.TransportationOrderViewSet, basename = 'transportation_order')
router.register(r'places', views.LoadOrDeliveryPlaceViewSet)
router.register(r'tanker_trailers', views.TankerTrailerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
