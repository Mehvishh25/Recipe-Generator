import streamlit as st
from style import page_style

# Import all your page modules
import welcome
import login
import signup
import main_page
import user_profile
import recipe_generator
import image_recipe_generator
import recipe_from_name

st.set_page_config(page_title="Recipe Genie", layout="wide")

# Apply custom styling
st.markdown(page_style, unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

# Logo and app name in sidebar
st.sidebar.title("Recipe Genie")
st.sidebar.markdown("---")

# Main navigation logic
if not st.session_state.logged_in:
    # Show only these options when not logged in
    pages = {
        "Welcome": welcome,
        "Login": login,
        "Sign Up": signup
    }
    
    # Default to welcome page for first-time visitors
    if st.session_state.current_page not in pages:
        st.session_state.current_page = "Welcome"
    
    # Simple navigation buttons for non-logged in users
    for page_name in pages:
        if st.sidebar.button(page_name):
            st.session_state.current_page = page_name
            # Force a rerun to show the selected page
            st.rerun()
    
    # Show the selected page
    if st.session_state.current_page in pages:
        pages[st.session_state.current_page].show()
    
else:
    # Full navigation when logged in
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    st.sidebar.markdown("---")
    
    # Navigation options for logged-in users
    pages = {
        "Dashboard": main_page,
        "Profile": user_profile,
        "Recipe Generator": recipe_generator,
        "Image Recipe Generator": image_recipe_generator,
        "Basic Recipe Generator":recipe_from_name,
        "Logout": None  # Special case handled below
    }
    
    # Create navigation buttons
    for page_name in pages:
        if st.sidebar.button(page_name):
            if page_name == "Logout":
                # Handle logout
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.current_page = "Welcome"
                st.rerun()
            else:
                st.session_state.current_page = page_name
                st.rerun()
    
    # Show the selected page
    if st.session_state.current_page in pages and pages[st.session_state.current_page] is not None:
        pages[st.session_state.current_page].show()