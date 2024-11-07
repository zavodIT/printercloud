# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def my_printers(request):
    # Example data - Replace this with your database query if needed
    user_printers = [
        {"name": "Printer 1", "status": "Online"},
        {"name": "Printer 2", "status": "Offline"},
        {"name": "Printer 3", "status": "Online"},
    ]

    context = {
        'user_printers': user_printers
    }
    return render(request, 'dashboard/my_printers.html', context)