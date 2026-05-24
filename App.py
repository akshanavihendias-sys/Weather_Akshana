from time import time

import requests
import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng




st.title("AKD Weather Dashboard")

st.subheader("Live Weather Data", divider="yellow")

country={
    "Sri Lanka": (6.9355, 80.9612,"lk"),
    "United Kingdom": (51.5074, -0.1278,"gb"),
    "India": (20.0, 78.0,"in"),
    "Australia": (-33.8688, 151.2093,"au"),
    "United States": (39.9526, -75.1652,"us")
}
st.sidebar.subheader("Weather data", divider="yellow")
option = st.sidebar.selectbox(
    "Select a Country", list(country.keys()))

latitude, longitude, country_code = country[option]


st.image(f"https://flagcdn.com/w320/{country_code}.png")
api_URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,pressure_msl,rain,showers&current=wind_speed_10m,rain,precipitation,snowfall,temperature_2m,is_day,cloud_cover,pressure_msl"
resp = requests.get(api_URL)
data = resp.json()


tempo = data["current"]["temperature_2m"]
wind = data["current"]["wind_speed_10m"]
st.sidebar.header(f"Latitude: {latitude}°N😊")
st.sidebar.header(f"Longitude: {longitude}°E😊")
st.sidebar.header(f"Temperature: {tempo}°C😊")
st.sidebar.header(f"Wind Speed: {wind} km/h😊")

hourly = st.sidebar .subheader("Hourly Weather Data", divider="yellow")
hourly_option = st.sidebar.selectbox(
    "Select a Weather Parameter", ["Temperature", "Pressure", "Rain", "Showers"])


col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", tempo, "°C😊")
col2.metric("Wind", wind, "km/h😊")
col3.metric("Pressure", data["current"]["pressure_msl"], "hPa😊")
col4.metric("Snowfall", data["current"]["snowfall"], "cm😊")


hourly_data = pd.DataFrame(
    {
        "Temperature": data["hourly"]["temperature_2m"],
        "Pressure": data["hourly"]["pressure_msl"],
        "Rain": data["hourly"]["rain"],
        "Showers": data["hourly"]["showers"]
    }
)
if hourly_option == "Temperature":
    st.line_chart(hourly_data["Temperature"], use_container_width=True)

elif hourly_option == "Pressure":
    st.line_chart(hourly_data["Pressure"], use_container_width=True)

elif hourly_option == "Rain":
    st.line_chart(hourly_data["Rain"], use_container_width=True)

else:
    st.line_chart(hourly_data["Showers"], use_container_width=True)    