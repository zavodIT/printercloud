import requests

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

    def upload_print_job_file(self, printer_id, job_id, file_path):
        """
        Uploads a file to a specific printer job on Epson Connect.

        :param printer_id: The ID of the printer
        :param job_id: The ID of the print job
        :param file_path: Path to the file to be uploaded
        :return: JSON response containing job ID, upload URI, and job status, or an error message.
        """
        url = f"{self.api_url}/printing/printers/{printer_id}/jobs/{job_id}/upload"

        # Prepare headers and files
        headers = self.headers.copy()
        headers['Content-Type'] = 'multipart/form-data'

        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            files = {'file': file}

            # Make the POST request
            response = requests.post(url, headers=headers, files=files)

            # Check response status
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.status_code, "message": response.text}