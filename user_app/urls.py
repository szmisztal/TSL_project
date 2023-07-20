from django.urls import path
from user_app import views

urlpatterns = [
    path('register/', views.sign_up, name = 'register'),
    path('login/', views.sign_in, name = 'login'),
    path('logout/', views.sign_out, name = 'logout'),
    path('users_list/', views.UsersListView.as_view(), name = 'users-list')
]
