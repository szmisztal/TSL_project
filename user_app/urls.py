from django.urls import path
from django.views.generic import TemplateView
from user_app import views

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'homepage'),
    path('register/', views.sign_up, name = 'register'),
    path('login/', views.sign_in, name = 'login'),
    path('logout/', views.sign_out, name = 'logout'),
    path('users_list/', views.UsersListView.as_view(), name = 'users-list')
]
