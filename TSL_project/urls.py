from django.contrib import admin
from django.urls import path, include
from logistician_app import urls as logistician_urls
from logistician_app.views import NewOrder, NewPlace, NewTanker
from user_app.views import HomepageView
from user_app import urls as user_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logistician/', include(logistician_urls.urlpatterns)),
    path('accounts/', include(user_urls.urlpatterns)),
    path('', HomepageView.as_view(), name = "homepage"),
    path('new_order/', NewOrder.as_view(), name = "new_order"),
    path('new_place/', NewPlace.as_view(), name = "new_place"),
    path('new_tanker/', NewTanker.as_view(), name = "new_tanker")
]
