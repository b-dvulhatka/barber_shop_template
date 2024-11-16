# app.py
import streamlit as st
import functions  # Import the functions module

phone_regex = r"\b\d{2}([8-9]\d{8}|[1-7]\d{7})\b"
email_regex = r"^([A-Za-z0-9]+[._-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"

# Set page title and favicon
st.set_page_config(page_title="Barber Shop", page_icon="💈")

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Initialize the database
functions.init_db()

# Sidebar Navigation
functions.login_section()  # Display the login/logout section at the top-left of the page

st.sidebar.title("Navigation")
if st.session_state.get("logged_in", False):
    if st.session_state.user_role == "manager":
        page = st.sidebar.radio("Go to", ["Home", "Services", "Book Appointment", "Gallery", "Manage Appointments", "User Management", "Contact Us"])
    elif st.session_state.user_role == "employee":
        page = st.sidebar.radio("Go to", ["Home", "Services", "Book Appointment", "Gallery", "Manage Appointments", "Contact Us"])
else:
    page = st.sidebar.radio("Go to", ["Home", "Services", "Book Appointment", "Gallery", "Contact Us"])

# Page Display Logic
if page == "Home":
    functions.home_page()
elif page == "Services":
    functions.services_page()
elif page == "Book Appointment":
    functions.booking_page()
elif page == "Gallery":
    functions.gallery_page()
elif page == "Manage Appointments" and st.session_state.logged_in:
    functions.manage_appointments_page()
elif page == "User Management" and st.session_state.logged_in and st.session_state.user_role == "manager":
    functions.user_management_page()
elif page == "Edit Profile" and st.session_state.logged_in:
    functions.edit_profile_page()
elif page == "Contact Us":
    functions.contact_page()
