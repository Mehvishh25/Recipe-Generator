import streamlit as st
import json
import os

def show():
    st.title("Sign Up")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("signup_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")

        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
                
            if len(password) < 6:
                st.error("Password must be at least 6 characters long.")
                return
                
            if not username:
                st.error("Username cannot be empty.")
                return
                
            # Create users.json if it doesn't exist or handle corrupted JSON
            users = {}
            if os.path.exists("users.json"):
                try:
                    with open("users.json", "r") as f:
                        file_content = f.read().strip()
                        if file_content:  # Check if file is not empty
                            users = json.loads(file_content)
                        # If empty, users remains an empty dict
                except json.JSONDecodeError:
                    # File exists but contains invalid JSON, start with empty dict
                    st.warning("User database was corrupted. Starting fresh.")
            
            # Rest of the function stays the same
            if username in users:
                st.error("Username already exists.")
            else:
                users[username] = {
                    "password": password,
                    "profile": {
                        "name": "",
                        "age": 25,
                        "height": 170,
                        "weight": 70,
                        "gender": "Male",
                        "chronic_diseases": [],
                        "allergies": [],
                        "nutrients_required": [],
                        "cuisines_liked": [],
                        "preferences": []
                    }
                }
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)

                st.success("Account created successfully!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "Dashboard"
                st.rerun()

        st.markdown("Already have an account?")
        # Keep the unique key
        if st.button("Login", key="signup_to_login_button"):
            st.session_state.current_page = "Login"
            st.rerun()