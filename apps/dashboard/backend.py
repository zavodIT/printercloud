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
        # Ensure all values are strings as required by the API
        data = {
            "printerId": str(printer_id),
            "printerName": str(printer_name),
            "printerType": str(printer_type),
            "printerLocation": str(printer_location)
        }

        # Debugging output to check what is being sent
        print("Sending request to API with data:", data)
        print("Using headers:", self.headers)

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Printer added successfully:", response.json())
            return {"success": True, "message": response.json().get("message", "Printer added successfully")}
        else:
            print(f"Failed to add printer. Status Code: {response.status_code}, Response: {response.text}")
            return {"success": False, "message": response.json().get("detail", "Failed to add printer")}