# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .backend import *

def my_printers(request):
    # Check if user is authenticated
    if 'user' not in request.session:
        return redirect(f"/login/?next={request.path}")

    # Initialize PrinterAPI instance
    api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api/user/profile"
    auth_token = settings.AUTH_TOKEN
    printer_api = PrinterAPI(api_url, auth_token)

    # Call get_printers to retrieve the list of printers
    response = printer_api.get_printers()

    if response["success"]:
        user_printers = response["data"]
    else:
        # If retrieval fails, set user_printers to an empty list and add an error message
        user_printers = []
        error_message = response["message"]

    context = {
        'user_printers': user_printers,
        'error_message': response.get("message") if not response["success"] else None
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
        api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api/user/profile"
        auth_token = settings.AUTH_TOKEN
        printer_api = PrinterAPI(api_url, auth_token)

        # Call add_printer method from PrinterAPI
        response = printer_api.add_printer(printer_id, printer_name, printer_type, printer_location)

        # Check the response and pass the appropriate message to the template
        if response and response.get("success"):
            return render(request, 'dashboard/add_printer.html', {'success_message': response["message"]})
        else:
            return render(request, 'dashboard/add_printer.html', {'error_message': response["message"]})

    # Render the add printer form if GET request
    return render(request, 'dashboard/add_printer.html')

# myapp/views.py
from django.shortcuts import render


def start_print(request):
    # Check if user is authenticated
    if 'user' not in request.session:
        return redirect('/login')

    # Initialize PrinterAPI and get printers
    api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api/user/profile"
    auth_token = settings.AUTH_TOKEN
    printer_api = PrinterAPI(api_url, auth_token)
    response = printer_api.get_printers()

    # Prepare printer data and log for debugging
    user_printers = response["data"] if response["success"] else []
    print("User Printers:", user_printers)  # Debugging: Check if printers are fetched

    if request.method == "POST":
        # Handle file upload and printer selection logic here
        document = request.FILES.get("document")
        selected_printer_id = request.POST.get("printer")

        # Process the document printing logic (e.g., save file, send to print API)

        # Show success message on successful print initiation
        return render(request, 'dashboard/start_print.html', {
            'user_printers': user_printers,
            'success_message': "Print job started successfully."
        })

    # Render the start print page with printers
    return render(request, 'dashboard/start_print.html', {
        'user_printers': user_printers
    })