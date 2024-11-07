# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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

@login_required
def add_printer(request):
    if request.method == "POST":
        # Handle form submission to add a new printer
        # For example, create a Printer object and save it to the database
        # Redirect to the My Printers page after saving
        return redirect('my_printers')

    # Render a form template for adding a printer
    return render(request, 'dashboard/add_printer.html')