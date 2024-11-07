# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Define the login URL
    path('callback/', views.callback, name='callback'),
    path('logout/', views.logout, name='logout'),
]