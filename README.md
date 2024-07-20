# ToDo Project

Welcome to the ToDo Project, a simple yet powerful application built with Django and Django REST Framework. This project includes user authentication and allows users to create, read, update, and delete (CRUD) their to-do items.

## Features

- **User Authentication**: Secure login and registration functionality.
- **CRUD Operations**: Create, view, update, and delete to-do items.
- **PostgreSQL Database**: Robust data storage using PostgreSQL.
- **API Endpoints**: RESTful API endpoints for all functionalities.
- **Responsive UI**: Easy-to-use web interface.

## Table of Contents

- [Getting Started](#getting-started)
- [Using the Application](#using-the-application)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL
- Virtualenv

### Installation

To get started with the ToDo Project, follow these steps:

1. **Clone the repository:**

   Open your terminal and run:
   ```sh
   git clone https://github.com/ssenichhh/ToDo-site.git
   cd todowo-project
   ```

2. **Set up the virtual environment:**

   Create and activate a virtual environment with the following commands:
   ```sh
   python -m venv django-env
   source django-env/bin/activate
   ```

3. **Set up the database:**

   Ensure you have PostgreSQL installed and running. Create a database and update the database settings in `todowo/settings.py` accordingly.

4. **Prepare the project:**

   Run the following commands to set up the project:
   ```sh
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

Open your browser and navigate to `http://127.0.0.1:8000/` to use the application.

## Using the Application

### User Registration and Login

- **Register**: Create a new account by providing a username and password.
- **Login**: Access your account using your username and password.

### Managing To-Do Items

Once logged in, you can:

- **Create**: Add new to-do items by clicking on "Create" and filling in the details.
- **Read**: View your current to-do items on the dashboard. Completed items can be viewed in the "Completed" section.
- **Update**: Modify your existing to-do items by clicking on them and updating the details.
- **Delete**: Remove to-do items by clicking on the delete button.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

