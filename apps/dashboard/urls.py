# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-printers/', views.my_printers, name='my_printers'),  # URL for My Printers
    path('add-printer/', views.add_printer, name='add_printer'),
    path('start-print/', views.start_print, name='start_print'),  # Add this line
    path('my-printers/<str:printer_id>/', views.printer_details, name='printer_details'),
    path('my-printers/<str:printer_id>/', views.printer_details, name='printer_details'),

    path('user-profiles/', views.user_profiles, name='user_profiles'),
    # other paths
    # other URLs...
]