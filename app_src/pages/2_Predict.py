import streamlit as st
import pandas as pd
import joblib
import yaml
import os
import random


def correct_path(path_type, name):
    config_path = os.path.join("..", "configs", "paths.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    path = config[path_type][name]
    full_path = os.path.join("..", path.replace("\\", "/"))
    return full_path


@st.cache_resource
def load_model():
    model_path = correct_path("artifacts_paths", "xg_model_path")
    model = joblib.load(model_path)
    return model


@st.cache_resource
def test_data():
    data_path = correct_path("data_paths", "test_data_path")
    test_data = pd.read_csv(data_path)
    cat_cols = test_data.select_dtypes(include=['object']).columns
    for col in cat_cols:
        test_data[col] = test_data[col].astype('category')
    return test_data


model = load_model()
test_df = test_data()


st.title("Rainfall Predictor")
st.write("Click the button below to load a random test sample and predict if it will rain or not.")


if st.button("Predict on Random Sample"):
    sample = test_df.sample(n=1, random_state=random.randint(0, 9999))
    with st.expander("Sample Features:"):
        st.dataframe(sample.T, use_container_width=True)
    

    predection_class = model.predict(sample)[0]
    predection_proba = model.predict_proba(sample)[0][1]

    predection_label = "Rain" if predection_class == 1 else "No Rain For Tomorrow!"

    st.subheader("🌤️ Prediction Result")
    if predection_class == 1:
        st.success(f"**Prediction: Rain 🌧️**\n\n**Confidence:** {predection_proba:.2%}")
    else:
        st.info(f"**Prediction: No Rain ☀️**\n\n**Confidence:** {(1 - predection_proba):.2%}")