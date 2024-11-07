# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-printers/', views.my_printers, name='my_printers'),  # URL for My Printers
    # other URLs...
]