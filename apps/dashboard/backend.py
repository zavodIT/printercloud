import requests
import tempfile
import subprocess
import json

class PrinterAPI:
    def __init__(self, api_url, auth_token):
        self.api_url = api_url
        self.auth_token = auth_token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def add_printer(self, printer_id, printer_name, printer_type, printer_location):
        # Construct the data payload
        data = {
            "printerId": str(printer_id),
            "printerName": str(printer_name),
            "printerType": str(printer_type),
            "printerLocation": str(printer_location)
        }

        # Make the POST request to add a printer
        response = requests.post(self.api_url + "/printer", headers=self.headers, json=data)

        # Check for a successful response
        if response.status_code == 200:
            return {"success": True, "message": response.json().get("message", "Printer added successfully")}
        else:
            # Return the error message from the API or a default error message
            return {"success": False, "message": response.json().get("message", "Failed to add printer")}

    def get_printers(self):
        response = requests.get(self.api_url + "/printers", headers=self.headers)

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "message": f"Failed to retrieve printers. Status Code: {response.status_code}"}

    def get_printer_details(self, printer_id):
        """
        Fetches details for a specific printer.

        :param printer_id: The ID of the printer
        :return: JSON response containing printer details or an error message
        """
        url = f"{self.api_url}/printers/{printer_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}


    def upload_print_job_file(self, printer_id, job_id, document):
        """
        Uploads a file to a specific printer job on Epson Connect.

        :param printer_id: The ID of the printer
        :param job_id: The ID of the print job
        :param document: The InMemoryUploadedFile to be uploaded
        :return: JSON response containing job ID, upload URI, and job status, or an error message.
        """
        url = f"{self.api_url}/printing/printers/{printer_id}/jobs/{job_id}/upload"

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(document.read())
            temp_file_path = temp_file.name

        # Construct the curl command to upload the file
        command = [
            "curl", "--request", "POST",
            "--url", url,
            "--header", "Accept: application/json",
            "--header", f"Authorization: Bearer {self.auth_token}",
            "--form", f"file=@{temp_file_path}"
        ]

        # Execute the curl command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Output debugging information
        print("Curl Command Output:", result.stdout)
        print("Curl Command Error:", result.stderr)

        # Parse and return the JSON response if successful
        if result.returncode == 0:
            try:
                response_json = json.loads(result.stdout)
                return response_json
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response from server", "details": result.stdout}
        else:
            return {"error": "Curl command failed", "details": result.stderr}

    def get_printed_documents(self, printer_id, profile_id):
        """
        Fetches a list of documents printed on a specific printer.

        :param printer_id: The ID of the printer
        :param profile_id: The profile ID associated with the user
        :return: A list of documents or an error message
        """
        url = f"{self.api_url}/user/profile/documents"
        params = {
            "printerId": printer_id,
            "profile_id": profile_id
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
