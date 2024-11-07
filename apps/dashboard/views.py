from django.shortcuts import render, redirect
from django.conf import settings
from .backend import PrinterAPI


def my_printers(request):
    if 'user' not in request.session:
        return redirect(f"/login/?next={request.path}")

    # Initialize PrinterAPI with base URL from settings
    printer_api = PrinterAPI(settings.BASE_API_URL, settings.AUTH_TOKEN)

    # Retrieve printers
    response = printer_api.get_printers()
    user_printers = response["data"] if response["success"] else []
    error_message = response.get("message") if not response["success"] else None

    context = {
        'user_printers': user_printers,
        'error_message': error_message
    }
    return render(request, 'dashboard/my_printers.html', context)


def add_printer(request):
    if request.method == "POST":
        printer_id = request.POST.get("printer_id")
        printer_name = request.POST.get("printer_name")
        printer_type = request.POST.get("printer_type")
        printer_location = request.POST.get("printer_location")

        # Initialize PrinterAPI instance with base URL from settings
        printer_api = PrinterAPI(settings.BASE_API_URL, settings.AUTH_TOKEN)

        response = printer_api.add_printer(printer_id, printer_name, printer_type, printer_location)
        message = response.get("message", "An error occurred.") if response else "Failed to add printer."

        return render(request, 'dashboard/add_printer.html', {
            'success_message' if response.get("success") else 'error_message': message
        })

    return render(request, 'dashboard/add_printer.html')


def start_print(request):
    if 'user' not in request.session:
        return redirect('/login')

    printer_api = PrinterAPI(settings.BASE_API_URL, settings.AUTH_TOKEN)
    response = printer_api.get_printers()
    user_printers = response["data"] if response["success"] else []

    if request.method == "POST":
        epson_api = PrinterAPI(settings.EPSON_API_URL, settings.AUTH_TOKEN)
        document = request.FILES.get("document")
        selected_printer_id = request.POST.get("printer")
        job_id = "111222333"

        if document and selected_printer_id:
            upload_response = epson_api.upload_print_job_file(selected_printer_id, job_id, document)
            message = upload_response.get("message", "Failed to create print job.")

            context = {
                'user_printers': user_printers,
                'success_message' if upload_response.get("job_status") == "CREATED" else 'error_message': message
            }
            return render(request, 'dashboard/start_print.html', context)

        error_message = "Please select a printer and upload a document."
        return render(request, 'dashboard/start_print.html', {
            'user_printers': user_printers,
            'error_message': error_message
        })

    return render(request, 'dashboard/start_print.html', {'user_printers': user_printers})


def printer_details(request, printer_id):
    printer_api = PrinterAPI(settings.BASE_API_URL, settings.AUTH_TOKEN)
    response = printer_api.get_printer_details(printer_id)
    printer = response.get("printer")
    error_message = response.get("message") if not printer else None

    printed_documents = printer_api.get_printed_documents(printer_id, profile_id="11222")

    context = {
        'printer': printer,
        'printed_documents': printed_documents,
        'error_message': error_message
    }
    return render(request, 'dashboard/printer_details.html', context)