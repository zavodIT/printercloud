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
    auth_token = settings.AUTH_TOKEN
    api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api/user/profile"
    printer_api = PrinterAPI(api_url, auth_token)
    response = printer_api.get_printers()
    user_printers = response["data"] if response["success"] else []

    if request.method == "POST":
        # Epson Connect API URL for uploading files
        epson_api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/epson-connect-printing-api"
        epson_api = PrinterAPI(epson_api_url, auth_token)

        # Get uploaded file and selected printer
        document = request.FILES.get("document")
        selected_printer_id = request.POST.get("printer")
        job_id = "111222333"  # For demonstration, should be unique per job

        if document and selected_printer_id:
            # Directly use the document for upload
            upload_response = epson_api.upload_print_job_file(selected_printer_id, job_id, document)

            # Check upload status
            if upload_response and "job_status" in upload_response and upload_response["job_status"] == "CREATED":
                success_message = f"Print job created successfully. Job ID: {upload_response['job_id']}"
                context = {'user_printers': user_printers, 'success_message': success_message}
            else:
                error_message = upload_response.get("message", "Failed to create print job.")
                context = {'user_printers': user_printers, 'error_message': error_message}
            return render(request, 'dashboard/start_print.html', context)

        else:
            error_message = "Please select a printer and upload a document."
            context = {'user_printers': user_printers, 'error_message': error_message}
            return render(request, 'dashboard/start_print.html', context)

    return render(request, 'dashboard/start_print.html', {'user_printers': user_printers})


from django.shortcuts import render

def printer_details(request, printer_id):
    # Initialize PrinterAPI instance
    api_url = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/auth0-google-api"
    auth_token = settings.AUTH_TOKEN
    printer_api = PrinterAPI(api_url, auth_token)

    # Mock printer information
    printer = {
        "printerName": "Office Printer",
        "printerType": "Laser",
        "printerLocation": "Room 101",
        "status": "Online",
        "printsThisMonth": 120
    }

    # Fetch printed documents for the specified printer
    printed_documents = printer_api.get_printed_documents(printer_id, profile_id="11222")

    context = {
        'printer': printer,
        'printed_documents': printed_documents
    }
    return render(request, 'dashboard/printer_details.html', context)