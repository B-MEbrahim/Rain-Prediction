import streamlit as st
import pandas as pd
import requests
import joblib
import yaml
import os



location_id = {
    "Albury": "IDCJDW2002",
    "BadgerysCreek": "IDCJDW2126",
    "Cobar": "IDCJDW2050",
    "CoffsHarbour": "IDCJDW2080",
    "Moree": "IDCJDW2084",
    "Newcastle": "IDCJDW2097",
    "NorahHead": "IDCJDW2096",
    "NorfolkIsland": "IDCJDW8002",
    "Penrith": "IDCJDW2127",
    "Richmond": "IDCJDW2128",
    "Sydney": "IDCJDW2129",
    "SydneyAirport": "IDCJDW2130",
    "WaggaWagga": "IDCJDW2139",
    "Williamtown": "IDCJDW2140",
    "Wollongong": "IDCJDW2141",
    "Canberra": "IDCJDW2801",
    "Tuggeranong": "IDCJDW2802",
    "Ballarat": "IDCJDW3033",
    "Bendigo": "IDCJDW3008",
    "Sale": "IDCJDW3035",
    "MelbourneAirport": "IDCJDW3036",
    "Melbourne": "IDCJDW3037",
    "Mildura": "IDCJDW3038",
    "Nhil": "IDCJDW3039",
    "Portland": "IDCJDW3040",
    "Watsonia": "IDCJDW3041",
    "Dartmoor": "IDCJDW3042",
    "Brisbane": "IDCJDW4019",
    "Cairns": "IDCJDW4020",
    "GoldCoast": "IDCJDW4021",
    "Townsville": "IDCJDW4022",
    "Adelaide": "IDCJDW5081",
    "MountGambier": "IDCJDW5003",
    "Nuriootpa": "IDCJDW5004",
    "Woomera": "IDCJDW5005",
    "Albany": "IDCJDW6111",
    "Witchcliffe": "IDCJDW6112",
    "PearceRAAF": "IDCJDW6113",
    "PerthAirport": "IDCJDW6114",
    "Perth": "IDCJDW6115",
    "SalmonGums": "IDCJDW6116",
    "Walpole": "IDCJDW6117",
    "Hobart": "IDCJDW7021",
    "Launceston": "IDCJDW7025",
    "AliceSprings": "IDCJDW8019",
    "Darwin": "IDCJDW8014",
    "Katherine": "IDCJDW8021",
    "Uluru": "IDCJDW8022"
}

# app title
st.title("Rainfall Predictor")

# load configuration paths
@st.cache_data
def correct_path(path_type, name):
    # Get the directory where the current script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the configs folder
    config_path = os.path.join(current_dir, "..", "..", "configs", "paths.yaml")
    config_path = os.path.normpath(config_path)
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    path = config[path_type][name]
    full_path = os.path.join(current_dir, "..", "..", path.replace("\\", "/"))
    return os.path.normpath(full_path)


# load the model
@st.cache_resource
def load_model():
    model_path = correct_path("artifacts_paths", "xg_model_path")
    model = joblib.load(model_path)
    return model

# user input
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Select a date", pd.to_datetime("today"))
with col2:
    selected_location = st.selectbox("Select a location", list(location_id.keys()))

selected_year = selected_date.strftime("%Y")
selected_month = selected_date.strftime("%m")
selected_day = selected_date.strftime("%d")

# fetch data
def fetch_data():
    data_url = f"https://reg.bom.gov.au/climate/dwo/{selected_year}{selected_month}/text/{location_id[selected_location]}.{selected_year}{selected_month}.csv"
    try:
        response = requests.get(data_url, timeout=10)
        response.raise_for_status()
        
        data_path = correct_path("dirs", "fetched_data")
        os.makedirs(data_path, exist_ok=True)
        file_path = os.path.join(data_path, f"{location_id[selected_location]}_{selected_year}{selected_month}.csv")
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download data: {str(e)}")
        st.write(data_url)
        return False
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return False


def prepare_csv():
    try:
        data_path = os.path.join(correct_path("dirs", "fetched_data"), 
                               f"{location_id[selected_location]}_{selected_year}{selected_month}.csv")
        with open(data_path, 'r', encoding='latin1') as f:
            lines = f.readlines()

        # Find the index of the first empty line
        for i, line in enumerate(lines):
            if line.strip() == "":
                break

        # Keep everything after the empty line
        cleaned_lines = lines[i+1:]

        with open(data_path, 'w', encoding='latin1') as f:
            f.writelines(cleaned_lines)
        return True
    except Exception as e:
        st.error(f"Error preparing CSV: {str(e)}")
        return False


@st.cache_data
def prepare_data():
    try:
        data_path = os.path.join(correct_path("dirs", "fetched_data"), f"{location_id[selected_location]}_{selected_year}{selected_month}.csv")
        df = pd.read_csv(data_path, encoding='latin1')
        df.drop(df.columns[0], axis=1, inplace=True)
        df['Location'] = selected_location 
        df.drop(columns=['Time of maximum wind gust'], inplace=True)

        df.rename(mapper={
            'Minimum temperature (°C)': 'MinTemp',
            'Maximum temperature (°C)': 'MaxTemp',
            'Rainfall (mm)': 'Rainfall',
            'Evaporation (mm)': 'Evaporation',
            'Sunshine (hours)': 'Sunshine',
            'Direction of maximum wind gust ': 'WindGustDir',
            'Speed of maximum wind gust (km/h)': 'WindGustSpeed',
            '9am Temperature (°C)': 'Temp9am',
            '9am relative humidity (%)': 'Humidity9am',
            '9am cloud amount (oktas)': 'Cloud9am',
            '9am wind direction': 'WindDir9am',
            '9am wind speed (km/h)': 'WindSpeed9am',
            '9am MSL pressure (hPa)': 'Pressure9am',
            '3pm Temperature (°C)': 'Temp3pm',
            '3pm relative humidity (%)': 'Humidity3pm',
            '3pm cloud amount (oktas)': 'Cloud3pm',
            '3pm wind direction': 'WindDir3pm',
            '3pm wind speed (km/h)': 'WindSpeed3pm',
            '3pm MSL pressure (hPa)': 'Pressure3pm',
            'Location': 'Location',
            'Date': 'Date'
        }, axis=1, inplace=True)

        df['RainToday'] = df['Rainfall'].apply(lambda x: 1 if pd.notnull(x) and x > 0 else 0)

        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Assuming 'data' is your DataFrame with a 'Date' column of datetime type
        df['day'] = df['Date'].dt.day
        df['month'] = df['Date'].dt.month
        df['year'] = df['Date'].dt.year

        # Create engineered features
        df['WindSpeed9am'] = pd.to_numeric(df['WindSpeed9am'], errors='coerce')
        df['TempDiff']      = df['MaxTemp'] - df['MinTemp']
        df['WindSpeedAvg']  = df[['WindSpeed9am', 'WindSpeed3pm']].mean(axis=1)
        df['HumidityDiff']  = df['Humidity3pm'] - df['Humidity9am']
        df['PressureDiff']  = df['Pressure3pm'] - df['Pressure9am']
        df['CloudCoverAvg'] = df[['Cloud9am', 'Cloud3pm']].mean(axis=1)
        df['RainToday']     = (df['Rainfall']    > 0).astype(int)
        df['WindGustDiff']  = df['WindGustSpeed'] - df['WindSpeedAvg']
        df = df[['Date', 'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation',
             'Sunshine', 'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
             'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
             'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
             'Temp3pm', 'RainToday', 'day', 'month', 'year', 'TempDiff', 
             'WindSpeedAvg', 'HumidityDiff', 'PressureDiff', 'CloudCoverAvg',
             'WindGustDiff']]
        
        df.drop(columns=['Date'], inplace=True)

        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            df[col] = df[col].astype('category')
        return df
    except Exception as e:
        st.error(f"Error preparing data: {str(e)}")
        return None


# predection
if st.button("Predict Rainfall"):
    with st.spinner("Fetching weather data..."):
        if not fetch_data():
            st.stop()
            
    with st.spinner("Preparing data..."):
        if not prepare_csv():
            st.stop()
            
        test_df = prepare_data()
        if test_df is None:
            st.stop()
            
    try:
        sample = test_df.loc[(test_df['year'] == int(selected_year)) & 
                            (test_df['month'] == int(selected_month)) & 
                            (test_df['day'] == int(selected_day))]
        if sample.empty:
            st.warning("No data available for the selected date")
            st.stop()
            
        with st.expander("Sample Features:"):
            display_df = sample.copy()
            cat_cols = display_df.select_dtypes(include=['category']).columns
            for col in cat_cols:
                display_df[col] = display_df[col].astype(str)
            problem_columns = ['WindGustDir', 'WindDir9am', 'WindDir3pm']
            display_df[problem_columns] = display_df[problem_columns].astype(str)
            
            # Prepare transposed dataframe with custom column names
            transposed = sample.T.reset_index()
            transposed.columns = ['Feature', 'Value']
            st.dataframe(transposed, use_container_width=True)
        
        model = load_model()
        prediction_class = model.predict(sample)[0]
        prediction_proba = model.predict_proba(sample)[0][1]

        st.subheader("Prediction Result")
        if prediction_class == 1:
            st.success(f"**Prediction:** Rain tomorrow\n\n**Confidence:** {prediction_proba:.2%}")
            st.balloons()
        else:
            st.info(f"**Prediction:** No rain tomorrow\n\n**Confidence:** {(1 - prediction_proba):.2%}")
            
    except Exception as e:
        st.write(f"Prediction failed: {str(e)}")