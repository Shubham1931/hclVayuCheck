import streamlit as st
def city_input(cities):
    """Create city selection input"""
    return st.selectbox(
        "Select City",
        options=cities,
        index=0
    )

def environmental_inputs():
    """Create environmental parameter inputs"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-20.0,
            max_value=50.0,
            value=25.0,
            step=0.1
        )
    
    with col2:
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0
        )
    
    with col3:
        wind_speed = st.number_input(
            "Wind Speed (km/h)",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=0.1
        )
    
    return temperature, humidity, wind_speed
