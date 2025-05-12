page_style = """<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8bbd0, #9b4dca);
    min-height: 100vh;
}
h1, h2, p {
    font-family: 'Helvetica', 'Arial', sans-serif;
}
h1 { 
    font-size: 2.5rem; 
    font-weight: 700; 
    color: #333; 
    text-align: center;
    margin-bottom: 1.5rem;
}
h2 { 
    font-size: 1.8rem; 
    color: #333; 
    margin-bottom: 1rem;
}
h3 {
    font-size: 1.3rem;
    color: #444;
    margin-bottom: 0.8rem;
}
p { 
    color: #333; 
    font-size: 1.1rem; 
    line-height: 1.5; 
}

.stTextInput > div > div > input {
    border-radius: 10px; 
    padding: 10px 15px;
    font-size: 16px; 
    background-color: white; 
    color: #333;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.stTextInput > label { 
    color: #333; 
    font-size: 1rem; 
    font-weight: 500; 
}

.stButton > button {
    background-color: #ff7043; 
    color: white;
    border-radius: 10px; 
    padding: 10px 0;
    font-size: 16px; 
    font-weight: 500; 
    width: 100%;
    cursor: pointer; 
    box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    transition: background-color 0.3s;
}
.stButton > button:hover {
    background-color: #ff5722;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    padding-top: 2rem;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
    background-color: transparent;
    color: #333;
    border: 1px solid #9b4dca;
    margin-bottom: 0.5rem;
    transition: all 0.3s;
}

[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background-color: rgba(155, 77, 202, 0.1);
    color: #9b4dca;
}

div[data-testid="stForm"] {
    background-color: rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

div[data-testid="column"] {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem;
}
</style>"""