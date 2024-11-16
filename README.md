
# Barber Shop Application

Welcome to the Barber Shop Application! This application is designed to manage a barber shop's operations, including booking appointments, managing services, and handling user access. The application is built using Streamlit for the frontend and SQLite for the database.

## Features

- **User Authentication**: Secure login system for managers and employees.
- **Appointment Booking**: Customers can book appointments by selecting services, dates, and times.
- **Service Management**: Managers can add, edit, and remove services offered by the barber shop.
- **User Management**: Managers can manage employee access and details.
- **Contact Information**: Display and manage the barber shop's contact information.
- **Gallery**: Upload and manage images for the gallery.

## Usage

- **Login**: Use the sidebar to log in as a manager or employee.
- **Navigation**: Use the sidebar to navigate between different pages such as Home, Services, Book Appointment, Gallery, Manage Appointments, User Management, and Contact Us.
- **Booking**: Customers can book appointments by selecting available services and time slots.
- **Management**: Managers can manage appointments, services, and user access through the respective pages.

## Code Structure

- **`app.py`**: Main application file that sets up the Streamlit interface and handles navigation.
- **`functions.py`**: Contains all the backend logic for database operations and page functionalities.
