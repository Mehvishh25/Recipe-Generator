import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# 🔐 API Key
GEMINI_API_KEY = "AIzaSyBb0yOnYLBoicKe8SEajKCeMxqqAzneyzI"
genai.configure(api_key=GEMINI_API_KEY)

# 🧠 Ingredient Predictor using Gemini Vision
def predict_ingredients_from_image(image):
    """
    Uses Gemini Vision model to identify ingredients in the image.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-vision')

    prompt = (
        "Look at this image of food or ingredients. "
        "List ONLY the key food ingredients you can clearly identify. "
        "Respond with a simple list, no explanations or extras."
    )

    response = model.generate_content([prompt, image])

    ingredients_text = response.text

    # Basic cleaning: split lines and strip dashes or bullets
    ingredients = [item.strip('- ').strip() for item in ingredients_text.split('\n') if item.strip()]

    return ingredients

# ✅ Prompt Generator for Recipe
def generate_recipe_prompt(ingredients, cuisine, meal_type, difficulty, time_limit, restrictions):
    restrictions_str = ", ".join(restrictions) if restrictions else "None"
    prompt = f"""
    You are a professional chef. Please generate **EXACTLY 5 distinct and creative recipes** in the following format:

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

    Preferences:
    - Ingredients: {', '.join(ingredients)}
    - Cuisine: {cuisine}
    - Meal type: {meal_type}
    - Difficulty: {difficulty}
    - Max time: {time_limit} minutes
    - Dietary restrictions: {restrictions_str}
    """
    return prompt

# 🧪 Recipe Parsing
def parse_recipes(recipe_text):
    pattern = r"\*\*Title\*\*:\s*(.*?)\n"
    matches = list(re.finditer(pattern, recipe_text))
    
    if not matches:
        return [recipe_text]
    
    recipes = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(recipe_text)
        recipe = recipe_text[start:end].strip()
        recipe = re.sub(r'\n+', '\n', recipe)
        recipes.append(recipe)
    
    return recipes[:5]

# 🎨 Page UI
def show():
    st.title("📸 AI Recipe Generator from Image")
    st.markdown("Upload an image of your food or ingredients, and get **5 custom recipes**!")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.subheader("Recipe Preferences")
        col1, col2 = st.columns(2)

        with col1:
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])
            difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"])
        with col2:
            prep_time = st.slider("Max Prep Time (minutes)", 10, 120, 30)
            cuisine_type = st.selectbox("Cuisine", ["Any", "Italian", "Mexican", "Indian", "Chinese", "American", "Mediterranean", "Thai", "Japanese"])

        dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb", "Low-Fat"])

        if st.button("Generate Recipe from Image"):
            with st.spinner("Analyzing image and cooking up recipes... 🍳"):
                try:
                    # Step 1: Identify ingredients using Gemini Vision
                    ingredients = predict_ingredients_from_image(image)
                    if not ingredients:
                        st.error("No ingredients detected in the image. Please try another photo.")
                        return

                    st.success(f"🧑‍🍳 Detected Ingredients: {', '.join(ingredients)}")

                    # Step 2: Generate recipe prompt
                    prompt = generate_recipe_prompt(
                        ingredients,
                        cuisine_type,
                        meal_type,
                        difficulty,
                        prep_time,
                        dietary_restrictions
                    )

                    # Step 3: Generate recipes using Gemini Text model
                    text_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = text_model.generate_content(prompt)
                    recipe_text = response.text

                    # Step 4: Parse and display recipes
                    recipes = parse_recipes(recipe_text)

                    st.success(f"🎉 Generated {len(recipes)} Recipes from Image!")
                    for recipe in recipes:
                        title_match = re.search(r'\*\*Title\*\*:\s*(.+)', recipe)
                        title = title_match.group(1).strip() if title_match else "No Title"
                        body = recipe.replace(f"**Title**: {title}", "").strip()

                        st.markdown(f"""
                        <div style="background-color: #f0f8ff; padding: 1rem; margin-bottom: 20px; border-radius: 12px;">
                            <h3 style="color: #d35400;">{title}</h3>
                            <pre style="white-space: pre-wrap;">{body}</pre>
                        </div>
                        """, unsafe_allow_html=True)

                    st.download_button("💾 Download All Recipes", recipe_text, file_name="recipes_from_image.txt", mime="text/plain")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    show()
