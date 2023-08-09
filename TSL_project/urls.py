from django.contrib import admin
from django.urls import path, include
from user_app import urls as user_urls
from logistician_app import urls as logistician_urls
from dispatcher_app import urls as dispatcher_urls
from driver_app import urls as driver_urls
from .views import HomepageView

urlpatterns = [
    path('', HomepageView.as_view(), name = 'homepage'),
    path('admin/', admin.site.urls),
    path('users/', include(user_urls.urlpatterns)),
    path('logistician/', include(logistician_urls.urlpatterns)),
    path('dispatcher/', include(dispatcher_urls.urlpatterns)),
    path('driver/', include(driver_urls.urlpatterns))
]
