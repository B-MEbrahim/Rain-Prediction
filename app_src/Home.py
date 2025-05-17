import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
import yaml

# Page config
st.set_page_config(layout="wide", page_title="RainSense Australia | Smart Rainfall Forecasting")

# Load Lottie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Safe config path
def correct_path(path_type, name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "..", "configs", "paths.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    path = config[path_type][name]
    full_path = os.path.join(base_dir, "..", path.replace("\\", "/"))
    return full_path



# Welcome and intro
with st.container():
    st.markdown("""
    <div class="welcome-box">
        <h3>Welcome to the Australian Rainfall Prediction Platform!</h3>
        <p>Explore insightful analytics and powerful machine learning models to forecast rainfall across Australia with precision.</p>
    </div>
    """, unsafe_allow_html=True)

    

# Load animation
hero_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_sk5h1kfn.json")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

.welcome-box {
    background: linear-gradient(120deg, #2980b9, #6dd5fa);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 1.5rem;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.feature-card {
    background: #fff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.cta-button {
    background-color: #e74c3c;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    border: none;
    text-decoration: none;
}

.cta-button:hover {
    background-color: #c0392b;
}
</style>
""", unsafe_allow_html=True)

# Animation column
col1, col2 = st.columns([2, 1])
with col1:
    st.title("Australian Rainfall Prediction")
    st.markdown("""
    This platform leverages advanced machine learning models to accurately predict rainfall levels across Australia.
    Our models are trained on historical weather data and use cutting-edge techniques for forecasting weather patterns.
    """)



with col2:
    if hero_animation:
        st_lottie(hero_animation, height=300, key="hero")
    else:
        st.warning("Animation failed to load. Check connection or try later.")

# Video section
gif_path = correct_path("artifacts_paths", "gif_path")
st.image(gif_path)

# How it works section
st.markdown("## How Our Prediction System Works")
step_cols = st.columns(4)
steps = [
    ("1. Data Collection", "Weather observations for over 10 years."),
    ("2. Feature Engineering", "Analyzing 20+ weather parameters."),
    ("3. Model Training", "Advanced ML algorithms."),
    ("4. Prediction", "Accurate rainfall forecasts."),
]

for col, (title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)



