# functions.py
import sqlite3
import streamlit as st
import re
import os
import time
from datetime import datetime, timedelta


phone_regex = r"\b\d{2}([8-9]\d{8}|[1-7]\d{7})\b"
email_regex = r"^([A-Za-z0-9]+[._-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"

# Database Setup
def init_db():
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    
    # Create Appointments Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            service TEXT,
            date TEXT,
            time TEXT
        )
    """)
    
    # Create Services Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price TEXT,
            image_path TEXT
        )
    """)
    # create barber shop info table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BARBER_SHOP_INFO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            phone TEXT,
            cell TEXT,
            mail TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_access_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT DEFAULT 'employee',
            login TEXT UNIQUE,  -- Ensure login is unique
            name TEXT,
            password TEXT,
            cell TEXT,
            mail TEXT
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO user_access_data (id, role, login, password)
        VALUES (?, 'manager', ?, ?)
    """, (1, "manager", "password123"))

    conn.commit()
    conn.close()


def validate_login(cursor, username, password):
    """
    Validates the login credentials against the database.
    Args:
        cursor: SQLite cursor for database interaction.
        username (str): The entered username.
        password (str): The entered password.
    Returns:
        dict or None: Returns user details as a dictionary if valid, otherwise None.
    """
    cursor.execute("""
        SELECT id, login, name, role FROM user_access_data
        WHERE login = ? AND password = ?
    """, (username, password))
    user = cursor.fetchone()

    if user:
        return {"id": user[0], "login": user[1], "name": user[2], "role": user[3]}
    return None


def update_manager__credentials(username, password, name, cell, mail):    # Update manager credentials
        conn = sqlite3.connect("barber_shop.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE user_access_data SET password = ?, name = ?, cell = ?, mail = ? WHERE id = ?", (password, username, name, cell, mail))
        conn.commit()
        conn.close()

def insert_employee_access(ename, epass, ecell, email):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_access_data (login, name, password, cell, mail) VALUES (?, ?, ?, ?, ?)",
                   (ename, ename.lower(), epass, ecell, email))
    conn.commit()
    conn.close()

def update_employee_access(ename, epass, ecell, email, id):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user_access_data SET name = ?, password = ?, cell = ?, mail = ? WHERE id = ?",
                   (ename, epass, ecell, email, id))
    conn.commit()
    conn.close()

def remove_employees_data(id):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_access_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def insert_barber_shop_info(address, phone, cell, mail):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO BARBER_SHOP_INFO (address, phone, cell, mail) VALUES (?, ?, ?, ?)",
                  (address, phone, cell, mail))
    conn.commit()
    conn.close()  # Close the connection after updating

def update_barber_shop_info(address, phone, cell, mail):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE BARBER_SHOP_INFO SET address = ?, phone = ?, cell = ?, mail = ?",
                  (address, phone, cell, mail))
    conn.commit()
    conn.close()  # Close the connection after updating

def edit_profile_page():
    st.title("Edit Profile")
    user_id = st.session_state.user_id  # Assuming user_id is stored in session_state during login

    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()

    # Get user details
    cursor.execute("SELECT name, cell, mail FROM user_access_data WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        ename = st.text_input("Name", value=user[0], key="edit_name")
        ecell = st.text_input("Phone", value=user[1], key="edit_phone")
        email = st.text_input("Email", value=user[2], key="edit_email")
        epass = st.text_input("Password", type="password", key="edit_password")

        if st.button("Update Profile"):
            if ename and ecell and email and epass:
                update_employee_access(ename, epass, ecell, email, user_id)
                st.success("Profile updated successfully!")
                # st.rerun()
            else:
                st.error("Please fill out all fields.")

def get_barber_shop_info():
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BARBER_SHOP_INFO")
    info = cursor.fetchall()
    conn.close()
    return info

# Functions to manage appointments
def add_appointment(name, contact, service, date, time):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (name, contact, service, date, time) VALUES (?, ?, ?, ?, ?)",
                   (name, contact, service, date, time))
    conn.commit()
    conn.close()

def remove_appoiments(id):    # Remove appointment by ID
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def get_booked_times(date):
    """Retrieve all booked times for a specific date."""
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM appointments WHERE date = ?", (date,))
    booked_times = [row[0] for row in cursor.fetchall()]
    conn.close()
    return booked_times

def update_services(price, image_path):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE services SET image_path = ? WHERE price = ?",
                   (image_path, price))
    conn.commit()
    conn.close()  # Close the connection after updating

def get_appointments():
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments ORDER BY date, time")
    appointments = cursor.fetchall()
    conn.close()
    return appointments

# Functions to manage services
def add_service(name, description, price, image_path):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (name, description, price, image_path) VALUES (?, ?, ?, ?)",
                   (name, description, price, image_path))
    conn.commit()
    conn.close()

def get_services():
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return services

def get_service_by_name():
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM services")
    service = cursor.fetchall()
    conn.close()
    return service

def get_service_price(service_name):
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM services WHERE name = ?", (service_name,))
    price = cursor.fetchone()
    conn.close()
    return price

def home_page():
    st.title("Welcome to Our Barber Shop 💈")

    st.write("High-quality grooming services for the modern gentleman. Book an appointment, explore our services, and get to know us!")
    st.image("uploads/main_page/barber_shop_image.jpg", use_container_width=True)  # Replace with your own image

def services_page():
    st.header("Our Services")
    services = get_services()
    
    if services:
        for service in services:
            st.subheader(service[1])  # Service name
            st.write(service[2])  # Service description
            st.write(f"Price: {service[3]}")
            if service[4]:  # Display the image if it exists
                st.image(service[4], use_container_width=True)
    else:
        st.write("No services available. Please check back later.")


# Booking Page
def booking_page():

    st.header("Book an Appointment")
    st.write("Select your preferred service, date, and time.")

    # Fetch services and prices
    service_names = list(map(lambda x: x[1], get_services()))
    service_prices = {x[1]: x[3] for x in get_services()}  # Dictionary of {service_name: price}
    selected_service = st.selectbox("Choose a Service", service_names)
    selected_price = service_prices[selected_service]

    # Display the price as a read-only field
    st.text_input("Price", value=f"${selected_price}", disabled=True)   
    date = st.date_input("Select Date", min_value=datetime.now().date())

    # Define the time range for available slots
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    
    # Fetch booked times for the selected date
    booked_times = get_booked_times(date.strftime("%Y-%m-%d"))
    
    # Generate available time slots
    available_times = [
        (start_time + timedelta(minutes=30 * i)).strftime("%H:%M")
        for i in range((end_time - start_time).seconds // 1800)
    ]
    
    # Filter out booked times
    available_times = [t for t in available_times if t not in booked_times]
    
    # Further filter times if the selected date is today
    if date == datetime.now().date():
        available_times = [
            t for t in available_times if datetime.strptime(t, "%H:%M").time() > datetime.now().time()
        ]

    # Check if there are any available times
    if available_times:
        # Display the available times as a select box, formatted as HH:MM
        timestamp = st.selectbox("Select Available Time", available_times)
    else:
        # Custom message if no times are available
        st.warning("No available time slots for the selected date. Please choose a different date.")
        return  # Exit if no times are available

    name = st.text_input("Your Name")
    if not name:
        st.warning("Please enter your name.")
    contact = st.text_input("Contact Information (Phone or Email)")
    if contact:
        if re.match(phone_regex, contact) or (re.match(email_regex, contact)):
            st.success("Contact information is valid.")
        else:
            st.error("Invalid contact information. Please enter a valid phone number or email address.")

    if st.button("Book Appointment"):
        if not name or not contact:
            st.error("Please fill out all fields.")
        else:
            add_appointment(name, contact, selected_service, date.strftime("%Y-%m-%d"), timestamp)
            st.success(f"Appointment booked for {name} on {date} at {timestamp} for a {selected_service}.")
            time.sleep(2)

# Gallery Page
def gallery_page():
    st.header("Gallery")
    st.write("Take a look at some of our work.")
    # Display the gallery images
    gallery_images = os.listdir("uploads/gallery")
    if gallery_images:
        for image in gallery_images:
            st.image(f"uploads/gallery/{image}", caption=image, use_container_width=True)
    else:
        st.write("No images available in the gallery.")

# Contact Page
def contact_page():
    st.header("Contact Us")
    st.write("Feel free to reach out!")
    
    barber_shop_data = get_barber_shop_info()
    if barber_shop_data:
        for info in barber_shop_data:  # Display the contact information
            st.write(f"📍 Address: {info[1]}" if info[1] else "Address not registred.")
            st.write(f"📞 Phone: {info[2]}" if info[2] else "Phone not registred.")
            st.write(f"📞 Cellphone: {info[3]}" if info[3] else "Cellphone not registred.")
            st.write(f"📧 Email: {info[4]}" if info[4] else "Email not registred.")

    if st.session_state.logged_in and st.session_state.user_role == "manager":
        st.subheader("Manage Contact Data")
        insert_address = st.text_input("Insert Address")
        insert_phone = st.text_input("Insert Phone")
        insert_cellphone = st.text_input("Insert Cellphone")
        insert_mail = st.text_input("Insert Email")
        if re.match(phone_regex, insert_cellphone) and (re.match(email_regex, insert_mail)):
            st.success("Contact information is valid.")
        else:
            st.error("Invalid contact information. Please enter a valid phone number or email address.")
        if st.button("Update Contact Data"):
                barber_shop_infos = get_barber_shop_info()
                if not barber_shop_infos:
                    insert_barber_shop_info(insert_address, insert_phone, insert_cellphone, insert_mail)
                    st.success("Contact data inserted successfully!")
                    time.sleep(1)  # Wait for a second to ensure the page refreshes
                    st.rerun()  # Refresh the page to show the home page
                else:
                    update_barber_shop_info(insert_address, insert_phone, insert_cellphone, insert_mail)
                    st.success("Contact data updated successfully!")
                    time.sleep(1)  # Wait for a second to ensure the page refreshes
                    st.rerun()  # Refresh the page to show the home page

# Login/Logout Section at the top-left
def login_section():
    if st.session_state.get("logged_in", False):
        st.sidebar.write(f"Logged in as {st.session_state.user_role.capitalize()}")
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_role = None
            st.session_state.user_name = None
            st.success("Successfully logged out.")
            time.sleep(1)  # Wait for a second to ensure the page refreshes
            st.rerun()
    else:
        st.sidebar.write("Manager Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            conn = sqlite3.connect("barber_shop.db")
            cursor = conn.cursor()
            user = validate_login(cursor, username, password)
            conn.close()
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.user_role = user["role"]  # Store user role
                st.session_state.user_name = user["name"]  # Store user name
                st.sidebar.success(f"Welcome, {user['name']}!")
                time.sleep(1)  # Wait for a second to ensure the page refreshes
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials. Please try again.")

def user_management_page():
    st.title("User Management")
    conn = sqlite3.connect("barber_shop.db")
    cursor = conn.cursor()

    # Display all users
    st.subheader("All Users")
    cursor.execute("SELECT id, login, name, cell, mail FROM user_access_data WHERE login != 'manager'")
    users = cursor.fetchall()

    for user in users:
        st.write(f"Login: {user[1]}, Name: {user[2]}, Phone: {user[3]}, Email: {user[4]}")
        if st.button(f"Remove User {user[0]}", key=f"remove_user_{user[0]}"):
            remove_employees_data(user[0])
            st.rerun()

    # Add a new user
    st.subheader("Add New Employee")
    ename = st.text_input("Name", key="add_name")
    epass = st.text_input("Password", type="password", key="add_password")
    ecell = st.text_input("Phone", key="add_phone")
    email = st.text_input("Email", key="add_email")

    if st.button("Add Employee"):
        if ename and epass and ecell and email:
            insert_employee_access(ename, epass, ecell, email)
            st.success("New employee added successfully!")
            st.rerun()
        else:
            st.error("Please fill out all fields.")


# Appointment Management Page and Service Management (Restricted Access)
def manage_appointments_page():
    st.header("Manage Appointments & Services")
    
    # Appointment Management
    st.subheader("Appointments")
    appointments = get_appointments()

    if appointments:
        for appt in appointments:
            # Display appointment details
            st.write(f"**Client Name:** {appt[1]} | **Service:** {appt[3]}")
            st.write(f"**Date:** {appt[4]} | **Time:** {appt[5]}")

            # Create a button for removing the appointment
            col1, col2 = st.columns([2, 1])  # Create columns for layout
            with col2:
                if st.button("❌ Remove", key=f"remove_{appt[0]}"):
                    # Call the function to remove the appointment
                    remove_appoiments(appt[0])
                    st.success(f"Appointment scheduled to date {appt[4]} at {appt[5]} removed successfully!")
                    time.sleep(5)  # Wait for a few seconds to ensure the page refreshes
                    st.rerun()

            st.write("---")
    else:
        st.write("No appointments booked yet.")
    if st.session_state.user_role == "manager":
        # Service Management
        st.subheader("Manage Services")
        service_name = st.text_input("Service Name")
        service_description = st.text_area("Service Description")
        service_price = st.text_input("Service Price")
        service_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        if st.button("Add Service"):
            if service_name and service_description and service_price and service_image:
                image_path = f"uploads/services/{service_image.name}"
                with open(image_path, "wb") as f:
                    f.write(service_image.getbuffer())
                add_service(service_name, service_description, service_price, image_path)
                st.success(f"Service '{service_name}' added successfully!")
            else:
                st.error("Please fill out all fields and upload an image.")
        
        # Gallery Image Upload Section
        st.subheader("Manage Gallery Images")
        uploaded_image = st.file_uploader("Choose an image for the gallery", type=["jpg", "jpeg", "png"])
        image_caption = st.text_input("Image Caption")
        
        if st.button("Add to Gallery"):
            if uploaded_image and image_caption:
                # Save uploaded image to the gallery folder
                image_path = f"uploads/gallery/{uploaded_image.name}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                st.success("Image uploaded successfully to the gallery!")
            else:
                st.error("Please upload an image and enter a caption.")
