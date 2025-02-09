import streamlit as st
import pandas as pd
from utils.data_generator import generate_historical_data, get_cities
from utils.predictor import AQIPredictor
from components.charts import create_historical_chart, create_gauge_chart
from components.inputs import city_input, environmental_inputs

# Page config
st.set_page_config(
    page_title="Air Quality Prediction Platform",
    page_icon="🌍",
    layout="wide"
)

# Load custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize predictor
predictor = AQIPredictor()

# Header
st.title("🌍 Air Quality Prediction Platform")
st.markdown("Predict and analyze air quality for cities worldwide")

# Main container
with st.container():
    # City selection and environmental inputs
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        selected_city = city_input(get_cities())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        temperature, humidity, wind_speed = environmental_inputs()
        st.markdown('</div>', unsafe_allow_html=True)

# Prediction section
if st.button("Predict Air Quality"):
    with st.spinner("Analyzing air quality..."):
        # Get prediction
        predicted_aqi = predictor.predict_aqi(temperature, humidity, wind_speed)
        aqi_level, level_color = predictor.get_aqi_level(predicted_aqi)
        
        # Display prediction
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                f'<div class="metric-card" style="border-left-color: {level_color}">'
                f'<h3>Predicted AQI</h3>'
                f'<h2 style="color: {level_color}">{predicted_aqi:.1f}</h2>'
                f'<p>Level: {aqi_level}</p>'
                '</div>',
                unsafe_allow_html=True
            )
            
        with col2:
            st.plotly_chart(
                create_gauge_chart(predicted_aqi),
                use_container_width=True
            )

# Historical data section
st.markdown("### Historical Data")
historical_data = generate_historical_data(selected_city)
st.plotly_chart(
    create_historical_chart(historical_data),
    use_container_width=True
)

# Data table
with st.expander("View Historical Data Table"):
    st.dataframe(
        historical_data.style.format({
            'aqi': '{:.1f}',
            'temperature': '{:.1f}',
            'humidity': '{:.1f}',
            'wind_speed': '{:.1f}'
        })
    )

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666666;">'
    'Air Quality Prediction Platform | Built with Streamlit'
    '</div>',
    unsafe_allow_html=True
)
