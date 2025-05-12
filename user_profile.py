import streamlit as st
import json
import os

def show():
    st.title("👤 Profile")

    # Check if user is logged in
    if not st.session_state.logged_in:
        st.error("Please log in first.")
        return

    username = st.session_state.username

    # Load user data
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
    else:
        users = {}

    if username not in users:
        st.error("User profile not found.")
        return

    profile = users[username].get("profile", {})

    # Profile form
    with st.form("profile_form"):
        st.subheader("Personal Information")
        name = st.text_input("Full Name", profile.get("name", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=int(profile.get("age", 25)))
            height = st.number_input("Height (cm)", min_value=50, max_value=250, value=int(profile.get("height", 170)))
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(profile.get("gender", "Male")))
            weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=int(profile.get("weight", 70)))
        
        st.subheader("Health Information")
        chronic_diseases = st.text_input("Chronic Diseases (comma-separated)", ','.join(profile.get("chronic_diseases", [])))
        allergies = st.text_input("Allergies (comma-separated)", ','.join(profile.get("allergies", [])))
        nutrients_required = st.text_input("Nutrients Required (comma-separated)", ','.join(profile.get("nutrients_required", [])))
        
        st.subheader("Food Preferences")
        cuisines_liked = st.text_input("Cuisines Liked (comma-separated)", ','.join(profile.get("cuisines_liked", [])))
        preferences = st.text_input("Other Preferences (comma-separated)", ','.join(profile.get("preferences", [])))
        
        submit = st.form_submit_button("Save Profile")

    if submit:
        users[username]["profile"] = {
            "name": name,
            "age": age,
            "height": height,
            "weight": weight,
            "gender": gender,
            "chronic_diseases": [item.strip() for item in chronic_diseases.split(',')] if chronic_diseases else [],
            "allergies": [item.strip() for item in allergies.split(',')] if allergies else [],
            "nutrients_required": [item.strip() for item in nutrients_required.split(',')] if nutrients_required else [],
            "cuisines_liked": [item.strip() for item in cuisines_liked.split(',')] if cuisines_liked else [],
            "preferences": [item.strip() for item in preferences.split(',')] if preferences else []
        }
        
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
            
        st.success("Profile saved successfully!")