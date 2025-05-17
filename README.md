# Rain Prediction Project - Team SkyCast

## Project Overview
The Rain Prediction Project aims to build an intelligent model capable of predicting whether it will rain tomorrow based on real-world weather data collected from Australian weather stations.  
The project leverages machine learning techniques to analyze various meteorological features such as temperature, humidity, wind speed, air pressure, and more, in order to make accurate predictions that assist in weather forecasting.


## Project Goal / Problem Statement

Many individuals and sectors rely on weather forecasts for daily or operational decision-making, including:

- **Individuals**: Planning their day, choosing appropriate clothing, or deciding whether to carry an umbrella.
- **Agriculture**: Scheduling irrigation and harvesting.
- **Transportation**: Minimizing risks caused by weather conditions

### Our main goal is:
To build a smart system that predicts whether it will rain tomorrow based on today’s weather data.

## Dataset
The dataset used for this project is the **"Rain in Australia"** dataset, sourced from Kaggle. It contains daily weather observations from various weather stations across Australia, spanning several years.

**Key Features:**
- Over 140,000 records with 23 meteorological variables, including:
  - Date, Location, Min/Max Temperature, Rainfall, Evaporation, Sunshine
  - Wind Gust Speed/Direction, Humidity, Pressure, Cloud Cover
  - RainToday (whether it rained today), RainTomorrow (target variable)
- The target variable, `RainTomorrow`, indicates whether it will rain the next day (Yes/No).


**Data Source:**  
[Kaggle - Rain in Australia](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package)

This dataset provides a comprehensive basis for training and evaluating machine learning models for rain prediction.


## How to Run the Project Locally

Follow the steps below to run the Rain Prediction app on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/B-MEbrahim/Rain-Prediction.git
cd Rain-Prediction
```

### 2. (Optional) Create and Activate a Virtual Environment
```bash
python -m venv env
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app.py
```

-------------
## Useful Links

- **Kaggle Notebook (EDA & Modeling):**  
  [https://www.kaggle.com/code/mohamedmahmoud111/rain-prediction-porject](https://www.kaggle.com/code/mohamedmahmoud111/rain-prediction-porject)

- **Live Streamlit App:**  
  [https://rain-prediction-xynsjsyukgjsyykngqqgqy.streamlit.app/](https://rain-prediction-xynsjsyukgjsyykngqqgqy.streamlit.app/)
## Team Members

- Hassan Abdelrazek 
- Mahmoud Ebrahim  
- Mohamed Elseragy
- Ahmed Fouad  
- Abdulrhman Hosny  
- Wageeh Abdelhameed  
