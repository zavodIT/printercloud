# PrinterCloud

PrinterCloud is a cloud-based print management solution built with Django. It enables remote management of printers,
tracking of print jobs, and user profile management, integrating Epson and Ambassador Blackbird APIs with secure
authentication via Auth0.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [License](#license)

## Features

- **Remote Printer Management**: Add, manage, and view printer details remotely.
- **User Profiles**: Access user profile information and print statistics.
- **Document Printing**: Upload documents and manage print jobs.
- **Authentication**: Secure login with Auth0.
- **API Integration**: Leverages Epson and Ambassador Blackbird APIs for enhanced functionality.

## Requirements

- Python 3.8+
- Django 3.2+
- Virtual environment (recommended)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/zavodIT/printercloud.git
   cd printercloud


2. **Set Up Virtual Environment**

    ```bash
    python3 -m venv env
    source env/bin/activate

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
   
## Configuration

	1.	Environment Variables

    DJANGO_SECRET_KEY=<your_django_secret_key>
    AUTH_TOKEN=<your_auth_token>
    BASE_API_URL=https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/printercloud-api
    AUTH0_CLIENT_ID=<your_auth0_client_id>
    AUTH0_CLIENT_SECRET=<your_auth0_client_secret>
    AUTH0_DOMAIN=<your_auth0_domain>

## Usage
    ```bash
    python manage.py runserver

## API Integration
PrinterCloud integrates with third-party APIs for enhanced printer management and tracking:

	•	Epson & Blackbird APIs: Utilized for managing print jobs and retrieving printer information.
	•	Auth0: Provides secure user authentication.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

