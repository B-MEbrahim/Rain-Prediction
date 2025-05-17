import streamlit as st
from streamlit_lottie import st_lottie
import requests

# -------------- Page Configuration --------------
st.set_page_config(page_title="About This Project", layout="wide")

# -------------- Load Animation from URL (.json only) --------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_weather =  load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_sk5h1kfn.json")


# -------------- Header Section with Animation --------------
header_col1, header_col2 = st.columns([1, 2])
with header_col1:
    if lottie_weather:
        st_lottie(lottie_weather, height=250, key="weather")
    else:
        st.error("Could not load animation.")
with header_col2:
    st.title("About This Project")
    st.markdown("""
    This project aims to predict whether it will rain tomorrow in various Australian locations using
                historical weather data collected from the Australian Bureau of Meteorology. 
                Leveraging machine learning, specifically an XGBoost classification model trained on 30 meteorological features
                (such as temperature, humidity, wind speed, and pressure), the system provides a binary prediction: Rain or No Rain.
    """)

st.markdown("---")

# -------------- Our Mission Section --------------
st.subheader("Our Mission")
st.markdown("""
Our goal is to provide accurate rainfall predictions across Australia using machine learning and historical weather data.

We aim to:
- Help farmers make informed agricultural decisions
- Support city planners with water resource management
- Assist researchers with climate studies
- Offer an interactive tool for weather enthusiasts
""")

st.markdown("---")

# -------------- Methodology Section --------------
st.subheader("Our Methodology")

method_cols = st.columns(4)
with method_cols[0]:
    st.markdown("**1. Data Collection**")
    st.markdown("- Bureau of Meteorology\n- 10+ years\n- 20+ weather features")

with method_cols[1]:
    st.markdown("**2. Data Cleaning**")
    st.markdown("- Missing values\n- Outlier detection\n- Feature engineering")

with method_cols[2]:
    st.markdown("**3. Exploratory Analysis**")
    st.markdown("- Visual insights\n- Correlation analysis\n- Summary statistics")

with method_cols[3]:
    st.markdown("**4. Model Building**")
    st.markdown("- Model training\n- Feature selection\n- Hyperparameter tuning")

st.markdown("---")

# -------------- Tools Used Section --------------
st.subheader("Tools Used")

tools = {
    "Python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    "Pandas": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg",
    "NumPy": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg",
    "Scikit-learn": "https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg",
    "XGBoost": "https://upload.wikimedia.org/wikipedia/commons/6/69/XGBoost_logo.png",
    "Streamlit": "https://streamlit.io/images/brand/streamlit-mark-color.svg"
}

# Animation style
animation_style = """
<style>
.tool-container:hover {
    transform: scale(1.1);
    transition: transform 0.3s ease;
}
</style>
"""
st.markdown(animation_style, unsafe_allow_html=True)

# Show tools in columns
tool_cols = st.columns(len(tools))
for col, (name, logo) in zip(tool_cols, tools.items()):
    with col:
        st.markdown(f"""
        <div class='tool-container' style='text-align: center; padding: 10px'>
            <img src='{logo}' width='50'><br>
            <span style='font-size:16px'>{name}</span>
        </div>
        """, unsafe_allow_html=True)


# -------------- Data Section --------------
st.markdown("---")
# Data Source / Citation section
st.markdown("## Data Source")
st.markdown("""
This project uses the [Australian weather dataset](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package) available on Kaggle, originally provided by Joseph Young.
""", unsafe_allow_html=True)


st.markdown("---")
# -------------- Contact Section --------------
st.subheader("Contact Us")
contact_cols = st.columns(3)

with contact_cols[0]:
    st.markdown("**Email**  \n[team@rainprediction.au](mailto:ha.razak.ds@gmail.com)")

with contact_cols[1]:
    st.markdown("**GitHub**  \n[github.com/rain-prediction](https://github.com/B-MEbrahim/Rain-Prediction)")

with contact_cols[2]:
    st.markdown("**Kaggle**  \n[kaggle.com/rain-prediction](https://www.kaggle.com/code/mohamedmahmoud111/rain-prediction-porject)")
