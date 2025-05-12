import streamlit as st
import json
import os

def show():
    st.title("Login")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            users = {}
            if not os.path.exists("users.json"):
                with open("users.json", "w") as f:
                    json.dump({}, f)
                st.error("No users registered. Please sign up first.")
                return
            else:
                try:
                    with open("users.json", "r") as f:
                        file_content = f.read().strip()
                        if file_content:  # Check if file is not empty
                            users = json.loads(file_content)
                        else:
                            st.error("No users registered. Please sign up first.")
                            return
                except json.JSONDecodeError:
                    # Handle corrupted JSON file
                    st.error("User database is corrupted. Please contact support.")
                    # Create a new empty users file
                    with open("users.json", "w") as f:
                        json.dump({}, f)
                    return

            if username in users and users[username]['password'] == password:
                st.success("Login successful!")
                # Update session state for logged-in user
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "Dashboard"
                # Force a rerun to refresh the sidebar and content
                st.rerun()
            else:
                st.error("Incorrect username or password.")

        st.markdown("Don't have an account yet?")
        # Keep the unique key
        if st.button("Sign Up", key="login_to_signup_button"):
            st.session_state.current_page = "Sign Up"
            st.rerun()