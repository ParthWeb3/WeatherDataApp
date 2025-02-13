import streamlit as st
import requests
import os

# Function to retrieve atmospheric conditions
def get_atmospheric_conditions(location):
    api_identifier = os.getenv("WEATHER_API_KEY", "3c1d901aba98438bacb44730251302")  # API key from environment variable
    endpoint_url = f"http://api.weatherapi.com/v1/current.json?key={api_identifier}&q={location}&aqi=no"

    try:
        server_response = requests.get(endpoint_url)
        server_response.raise_for_status()  # Detect HTTP errors
        weather_packet = server_response.json()

        if "error" in weather_packet:
            return None, weather_packet["error"]["message"]

        environmental_data = {
            "Location": weather_packet["location"]["name"],
            "Territory": weather_packet["location"]["country"],
            "Air_Temperature": f"{weather_packet['current']['temp_c']}°C",
            "Apparent_Temperature": f"{weather_packet['current']['feelslike_c']}°C",
            "Water_Vapor": f"{weather_packet['current']['humidity']}%",
            "Stress": f"{weather_packet['current']['pressure_mb']} hPa",
            "Air_Motion": f"{weather_packet['current']['wind_kph']} kph",
            "Sky": weather_packet["current"]["condition"]["text"],
            "Sky_Icon": weather_packet["current"]["condition"]["icon"],
            "Solar_Index": weather_packet["current"]["uv"],
            "Observation_Range": f"{weather_packet['current']['vis_km']} km"
        }

        return environmental_data, None

    except requests.exceptions.RequestException as e:
        return None, f"Service request failure: {e}"

# Streamlit application interface
st.title("🌍 Global Weather Viewer")
st.markdown("### Enter a location to view current atmospheric conditions.")

user_location = st.text_input("Enter Location", "London")

if st.button("Display Conditions"):
    conditions, error_message = get_atmospheric_conditions(user_location)

    if error_message:
        st.error(f"Attention: {error_message}")
    else:
        row_1, row_2 = st.columns([3, 2])

        with row_1:
            st.subheader(f"Current Conditions: {conditions['Location']}, {conditions['Territory']}")
            st.write(f"**Sky Overview:** {conditions['Sky']}")

        with row_2:
            st.image(f"http:{conditions['Sky_Icon']}", width=90)

        st.write("---")
        col_1, col_2, col_3 = st.columns(3)
        col_4, col_5, col_6 = st.columns(3)

        with col_1:
            st.metric("🌡 Air Temperature", conditions["Air_Temperature"])
        with col_2:
            st.metric("🤒 Apparent Temperature", conditions["Apparent_Temperature"])
        with col_3:
            st.metric("💧 Water Vapor", conditions["Water_Vapor"])
        with col_4:
            st.metric("💨 Air Motion", conditions["Air_Motion"])
        with col_5:
            st.metric("🔵 Stress", conditions["Stress"])
        with col_6:
            st.metric("☀️ Solar Index", conditions["Solar_Index"])

        st.write(f"**Observation Range:** {conditions['Observation_Range']}")

st.sidebar.info("I hope you find joy in exploring global weather patterns!")
st.sidebar.write("Developed by Parth K")