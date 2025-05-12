import streamlit as st
from style import page_style

def show():
    st.title("Welcome to Recipe Genie!")
    st.subheader("Find recipes tailored to your health and preferences")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Recipe Genie helps you:
        * Find recipes based on your dietary needs
        * Track your favorite recipes
        * Get personalized recommendations
        * Explore new cuisines and flavors
        
        Get started by logging in or creating a new account!
        """)
    
    with col2:
        st.image("https://via.placeholder.com/300x200?text=Recipe+Genie", use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("Login", use_container_width=True):
            st.session_state.current_page = "Login"
            st.rerun()
    
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.current_page = "Sign Up"
            st.rerun()