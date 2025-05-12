import streamlit as st
import google.generativeai as genai
import re

# 🔐 Your Gemini API Key
GEMINI_API_KEY = "AIzaSyBb0yOnYLBoicKe8SEajKCeMxqqAzneyzI"
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Generate Prompt from Dish Name (Only 1 Recipe)
def generate_recipe_prompt(dish_name):
    prompt = f"""
    You are a professional chef. Please generate **1 recipe** based on the dish name: **{dish_name}**.

    ---
    **Title**: Recipe Name  
    **Ingredients list**:  
    - List with quantities  
    **Instructions**:  
    - Step-by-step numbered  
    **Estimated Nutrition Info**:  
    - Calories, protein, fat, carbs  
    **Fun Gen-Z Humor**:  
    - End with a Gen-Z joke or emoji
    ---
    """
    return prompt

# ✅ Parse the Recipe from Gemini Response
def parse_recipe(recipe_text):
    pattern = r"\*\*Title\*\*:\s*(.*?)\n"
    matches = list(re.finditer(pattern, recipe_text))
    
    if not matches:
        return recipe_text.strip()

    # Extract the single recipe
    start = matches[0].start()
    end = len(recipe_text)  # Only take the first recipe
    recipe = recipe_text[start:end].strip()
    recipe = re.sub(r'\n+', '\n', recipe)
    
    return recipe

# 🎨 Streamlit App UI
st.title("🍝 AI Recipe Generator by Dish Name")
st.markdown("Enter a dish name (like **pasta**, **chicken tikka**, or **ramen**) and get a **single creative recipe**!")

dish_name = st.text_input("Enter Dish Name", placeholder="e.g., pasta, chicken tikka, ramen")

if st.button("Generate Recipe"):
    if not dish_name.strip():
        st.warning("⚠ Please enter a dish name!")
    else:
        with st.spinner("Cooking up your recipe... 🍽️"):
            prompt = generate_recipe_prompt(dish_name)

            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                recipe_text = response.text
            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")
                st.stop()

            recipe = parse_recipe(recipe_text)
            st.success(f"🎉 Generated Recipe for **{dish_name}**!")

            st.markdown(f"""
            <div style="background-color: #f0f8ff; padding: 1rem; margin-bottom: 20px; border-radius: 12px;">
                <h3 style="color: #27ae60;">{dish_name.title()} Recipe</h3>
                <pre style="white-space: pre-wrap;">{recipe}</pre>
            </div>
            """, unsafe_allow_html=True)

            st.download_button("💾 Download Recipe", recipe_text, file_name=f"recipe_for_{dish_name}.txt", mime="text/plain")
