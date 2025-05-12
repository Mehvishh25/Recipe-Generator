import streamlit as st
import google.generativeai as genai
import re

# 🔐 API Key
GEMINI_API_KEY = "AIzaSyBb0yOnYLBoicKe8SEajKCeMxqqAzneyzI"
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Prompt Generator
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

# 🧠 Gemini API Call
def generate_recipe_with_gemini(ingredients, cuisine, meal_type, difficulty, time_limit, restrictions):
    prompt = generate_recipe_prompt(ingredients, cuisine, meal_type, difficulty, time_limit, restrictions)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating recipe: {str(e)}"

# 🧪 Recipe Parsing
def parse_recipes(recipe_text):
    pattern = r"\*\*Title\*\*:\s*(.*?)\n"
    matches = list(re.finditer(pattern, recipe_text))
    
    if not matches:
        return [recipe_text]  # fallback
    
    recipes = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(recipe_text)
        recipe = recipe_text[start:end].strip()
        
        # Remove excessive newlines within each recipe
        recipe = re.sub(r'\n+', '\n', recipe)  # replace multiple newlines with one
        
        recipes.append(recipe)
    
    return recipes[:5]  # return ONLY 5

# 🎨 UI
def show():
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8f8f0;
        }
        .recipe-container {
            background-color: #e6f7ff;
            padding: 1.5rem;
            margin-bottom: 25px;
            border-radius: 12px;
            border: 1px solid #b3e0ff;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
        }
        .recipe-title {
            color: #d35400;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 12px;
        }
        .recipe-body {
            color: #2c3e50;
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🍽️ AI-Powered Recipe Generator")
    st.markdown("Get 5 custom recipes based on your ingredients and preferences.")

    st.subheader("🧑‍🍳 Recipe Preferences")
    col1, col2 = st.columns(2)

    with col1:
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"])
    with col2:
        prep_time = st.slider("Max Prep Time (minutes)", 10, 120, 30)
        cuisine_type = st.selectbox("Cuisine", ["Any", "Italian", "Mexican", "Indian", "Chinese", "American", "Mediterranean", "Thai", "Japanese"])

    dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb", "Low-Fat"])
    ingredients_input = st.text_area("🥕 Ingredients you have (comma-separated)").strip()

    if st.button("Generate Recipe"):
        if not ingredients_input:
            st.warning("Please enter some ingredients.")
            return

        ingredients_list = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        with st.spinner("Cooking up your recipes... 🍳"):
            recipe_text = generate_recipe_with_gemini(
                ingredients=ingredients_list,
                cuisine=cuisine_type,
                meal_type=meal_type,
                difficulty=difficulty,
                time_limit=prep_time,
                restrictions=dietary_restrictions
            )

        if recipe_text.startswith("Error"):
            st.error(recipe_text)
            return

        recipes = parse_recipes(recipe_text)

        st.success(f"🎉 Generated {len(recipes)} Recipes!")
        for recipe in recipes:
            title_match = re.search(r'\*\*Title\*\*:\s*(.+)', recipe)
            title = title_match.group(1).strip() if title_match else "No Title"
            body = recipe.replace(f"**Title**: {title}", "").strip()

            st.markdown(f"""
            <div class="recipe-container">
                <div class="recipe-title">{title}</div>
                <div class="recipe-body">{body}</div>
            </div>
            """, unsafe_allow_html=True)

        st.download_button("💾 Download All Recipes", recipe_text, file_name="recipes.txt", mime="text/plain")

# 🚀 Run App
if __name__ == "__main__":
    show()
