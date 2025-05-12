import streamlit as st

def show():
    st.title("Dashboard")
    
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return
        
    username = st.session_state.username
    
    st.markdown(f"### Welcome to your Recipe Dashboard, {username}!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Recipe Stats")
        st.metric("Saved Recipes", "0")
        st.metric("Favorite Cuisines", "0")
        st.metric("Health Score", "N/A")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Generate New Recipe"):
            st.session_state.current_page = "Recipe Generator"
            st.rerun()
        if st.button("Update Profile"):
            st.session_state.current_page = "Profile"
            st.rerun()
    
    st.subheader("Recent Recipes")
    st.info("You haven't generated any recipes yet. Try the Recipe Generator to get started!")