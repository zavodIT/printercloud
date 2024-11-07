# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .backend import *

def my_printers(request):

    if 'user' not in request.session:
        return redirect(f"/login/?next={request.path}")
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


from django.shortcuts import render, redirect
from django.conf import settings


def add_printer(request):
    if request.method == "POST":
        # Get form data from the request
        printer_id = request.POST.get("printer_id")
        printer_name = request.POST.get("printer_name")
        printer_type = request.POST.get("printer_type")
        printer_location = request.POST.get("printer_location")

        # Initialize PrinterAPI instance
        api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api/user/profile/printer"
        auth_token = settings.PRINTER_AUTH_TOKEN  # Make sure this token is securely stored in settings
        printer_api = PrinterAPI(api_url, auth_token)

        # Call add_printer method from PrinterAPI
        response = printer_api.add_printer(printer_id, printer_name, printer_type, printer_location)

        # Pass the message to the template based on success or failure
        if response["success"]:
            return render(request, 'dashboard/add_printer.html', {'success_message': response["message"]})
        else:
            return render(request, 'dashboard/add_printer.html', {'error_message': response["message"]})

    # Render the add printer form if GET request
    return render(request, 'dashboard/add_printer.html')