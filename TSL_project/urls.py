from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from logistician_app import urls as logistician_urls
from dispatcher_app import urls as dispatcher_urls
from user_app import urls as user_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    path('admin/', admin.site.urls),
    path('users/', include(user_urls.urlpatterns)),
    path('logistician/', include(logistician_urls.urlpatterns)),
    path('dispatcher/', include(dispatcher_urls.urlpatterns))
]
