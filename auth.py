import streamlit as st

# In-memory User Database (used for demo purposes)
users_db = {}

def init_user_db():
    """Initialize session state for user login"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

def signup_page():
    """Signup page for creating a new account"""
    st.title("Sign Up")
    username = st.text_input("Enter Gmail (Username)", placeholder="e.g. user@gmail.com")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif not username.endswith('@gmail.com'):
            st.error("Enter a valid Gmail address.")
        elif not first_name or not last_name:
            st.error("First Name and Last Name cannot be empty!")
        else:
            # Store user data
            users_db[username] = {
                "first_name": first_name,
                "last_name": last_name,
                "password": password
            }
            # Set session state to logged in
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Account created successfully! Welcome {first_name} {last_name}!")
            st.rerun()  # Rerun the app to show the logged-in view

def login_page():
    """Login page to authenticate existing users"""
    st.title("Login")
    username = st.text_input("Username (Gmail)", placeholder="e.g. user@gmail.com")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users_db and users_db[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back {users_db[username]['first_name']} {users_db[username]['last_name']}!")
            st.rerun()  # Rerun the app to show the logged-in view
        else:
            st.error("Invalid credentials. Please try again.")
