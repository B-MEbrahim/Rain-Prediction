# EDA Page
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import yaml
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests


# Page config
st.set_page_config(
    page_title="Data Explorer | Rainfall Prediction",
    
    layout="wide"
)


def correct_path(path_type, name):
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(repo_root, "configs", "paths.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    path = config[path_type][name]
    full_path = os.path.join(repo_root, path.replace("\\", "/"))
    return full_path


# Load CSS and animations
@st.cache_data
def load_css():
    styles_path = correct_path("artifacts_paths", "styles_path")
    with open(styles_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_weather =  load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_sk5h1kfn.json")


# Load data
@st.cache_data
def load_data():
    data_path = correct_path("data_paths", "cleaned_dahboard_data")
    df = pd.read_csv(data_path)
    if 'year' not in df.columns or 'month' not in df.columns:
        st.error("Columns 'year' and 'month' are required in your dataset.")
        st.stop()
    return df

# Load external files and data
df = load_data()
load_css()

# Sidebar filters
with st.sidebar:
    st.title(" Filters")
    st.markdown("Customize the data views below:")

    locations = sorted(df['Location'].unique())
    selected_locations = st.multiselect(
        "Select Locations",
        locations,
        default=["Sydney", "Melbourne", "Brisbane"]
    )

    years = sorted(df['year'].unique())
    year_range = st.slider(
        "Select Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(2015, 2020)
    )

    st.markdown("---")
    st.markdown("""
    <div class="sidebar-tip">
        <h4>💡 Pro Tip</h4>
        <p>Hover over charts for detailed values. Click legend items to toggle visibility.</p>
    </div>
    """, unsafe_allow_html=True)

# Filter data
filtered_df = df[
    (df['Location'].isin(selected_locations)) &
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1])
].copy()

# Header
st.markdown("""
<div class="header-section">
    <h1 class="page-title">Weather Data Explorer</h1>
    <p class="page-subtitle">Interactive visualizations of Australia's historical weather patterns</p>
</div>
""", unsafe_allow_html=True)

# the video is in the home page.
# video_path = correct_path("artifacts_paths", r"video_path")

# # check if video exists
# if os.path.exists(video_path):
#     html_code = f"""
#     <video width="100%" height="auto" autoplay loop muted>
#         <source src="file:///{video_path}" type="video/mp4">
#         Your browser does not support the video tag.
#     </video>
#     """
#     components.html(html_code)
# else:
#     st.error("Error loading the video.")
# --- Map section (first) ---
# --- Geographic Distribution Section ---
# --- Geographic Distribution Section ---
st.markdown("---")
with st.expander(" Geographic Distribution", expanded=True):
    st.subheader(" Rainfall & Weather Overview on Map")

    lottie_map = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jzviyhjn.json")
    if lottie_map:
        st_lottie(lottie_map, height=120, key="mapIcon")

    if {'Latitude', 'Longitude'}.issubset(filtered_df.columns):
        if not filtered_df.empty:
            location_df = filtered_df.dropna(subset=["Latitude", "Longitude"])

            if not location_df.empty:
                map_df = location_df.groupby('Location').agg({
                    'Rainfall': 'mean',
                    'MaxTemp': 'mean',
                    'MinTemp': 'mean',
                    'Sunshine': 'mean',
                    'Humidity3pm': 'mean',
                    'Latitude': 'first',
                    'Longitude': 'first'
                }).reset_index()

                # Debug: 
                st.write(" Map Data Sample:", map_df.head())

                fig = px.scatter_mapbox(
                    map_df,
                    lat="Latitude",
                    lon="Longitude",
                    size="Rainfall",
                    color="Rainfall",
                    hover_name="Location",
                    hover_data={
                        "Rainfall": ':.1f',
                        "MaxTemp": ':.1f',
                        "MinTemp": ':.1f',
                        "Sunshine": ':.1f',
                        "Humidity3pm": ':.0f',
                        "Latitude": False,
                        "Longitude": False
                    },
                    color_continuous_scale=px.colors.sequential.Blues,
                    mapbox_style="open-street-map",  
                    zoom=4,
                    size_max=40,
                    title=" Rainfall Intensity & Climate Patterns Across Australia"
                )

                fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(" No valid location data (Latitude/Longitude) after filtering.")
        else:
            st.warning(" No data available for the selected filters.")
    else:
        st.error(" Required columns 'Latitude' and 'Longitude' are missing in your dataset.")

# Add weather-themed animation before charts
lottie_weather = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_x62chJ.json")
if lottie_weather:
    st_lottie(lottie_weather, height=120, key="weather_intro")

# Rainfall Section
if filtered_df.empty:
    st.warning("No data matches your filters. Please adjust your selection.")
else:
    st.markdown("##  Rainfall Patterns")
    with st.expander("Rainfall Analysis", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st_lottie(load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_sk5h1kfn.json"), height=150, key="chart1")
            st.markdown("""
            <div class="info-card">
                <h3>Rainfall Insights</h3>
                <p>Explore how rainfall varies by location, season, and other weather factors.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            tab1, tab2 = st.tabs([" By Location", " By Month"]) #tab3: " Rain Today vs Tomorrow"])
            with tab1:
                fig = px.bar(
                    filtered_df.groupby('Location')['Rainfall'].mean().reset_index(),
                    x='Location', y='Rainfall',
                    title="Average Rainfall by Location",
                    color='Location'
                )
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                fig = px.line(
                    filtered_df.groupby(['month', 'Location'])['Rainfall'].mean().reset_index(),
                    x='month', y='Rainfall',
                    color='Location',
                    title="Monthly Rainfall Trends",
                    labels={'month': 'Month', 'Rainfall': 'Average Rainfall (mm)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            # with tab3:
            #     fig = px.sunburst(
            #         filtered_df,
            #         path=['RainToday', 'RainTomorrow'],
            #         title="Rain Today vs Rain Tomorrow"
            #     )
            #     st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    st.markdown("##  Temperature Trends")

    # Generate consistent color map
    locations = filtered_df['Location'].unique()
    color_sequence = px.colors.qualitative.Plotly  # Or use other palettes
    color_map = {loc: color_sequence[i % len(color_sequence)] for i, loc in enumerate(locations)}

    # with st.expander("Temperature Analysis"):
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(
            filtered_df,
            x='MaxTemp', y='MinTemp',
            color='Location',
            title="Max vs Min Temperature",
            trendline="lowess",
            opacity=0.4,
            color_discrete_map=color_map  
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure()
        for location in filtered_df['Location'].unique():
            fig.add_trace(go.Box(
                y=filtered_df[filtered_df['Location'] == location]['MaxTemp'],
                name=location,
                marker=dict(color=color_map[location]),
                boxpoints=False  # Hide individual outlier points
            ))

        fig.update_layout(
            title="Temperature Distribution by Location",
            showlegend=True,
            legend_title="Location"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("##  Wind Analysis")
    # with st.expander("Wind Direction and Speed"):
    col1, col2 = st.columns(2)
    with col1:
            fig = px.bar_polar(
                filtered_df,
                r="WindGustSpeed",
                theta="WindGustDir",
                color="Location",
                title="Wind Gust Direction and Speed",
                color_discrete_map=color_map,
                start_angle=112,
                template="presentation" # Other options include "plotly", "ggplot2", "seaborn", "simple_white", "none", 'xgridoff', 'presentation'.
            )
            st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.histogram(
            filtered_df,
            x="WindDir3pm",
            color="RainTomorrow",
            title="Wind Direction at 3pm vs Rainfall Tomorrow",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

# Data summary section
st.markdown("---")
# with st.expander(" Data Summary"):
st.dataframe(filtered_df.describe())
st.download_button(
    label="Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_weather_data.csv",
    mime="text/csv"
)