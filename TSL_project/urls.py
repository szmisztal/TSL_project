from django.contrib import admin
from django.urls import path, include
from logistician_app import urls as logistician_urls
from user_app import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logistician/', include(logistician_urls.urlpatterns)),
    path('users/', include(user_urls.urlpatterns)),
]
