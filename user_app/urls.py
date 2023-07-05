from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from user_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
