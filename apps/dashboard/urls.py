# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-printers/', views.my_printers, name='my_printers'),  # URL for My Printers
    path('add-printer/', views.add_printer, name='add_printer'),
    # other URLs...
]