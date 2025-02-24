import streamlit as st
import pandas as pd
from utils.data_generator import get_historical_data, get_cities
from utils.predictor import AQIPredictor
from utils.database import get_db
from components.charts import create_historical_chart, create_gauge_chart
from components.inputs import city_input, environmental_inputs
import base64

# Initialize database session
db = next(get_db())

# Page config
st.set_page_config(
    page_title="Air Quality Prediction Platform",
    page_icon="🌍",
    layout="wide"
)
# Function to encode local image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Convert local image to base64
image_base64 = get_base64_image("वाU_check_20250224_210949_0000_prev_ui-removebg-preview.png")


# Function to set background image
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("https://rs.tutiempo.net/i/css/nube-fondo.jpg") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the background
set_background()


# Apply custom CSS to remove top margin from the header

# Load custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize predictor
predictor = AQIPredictor()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Karla:ital,wght@0,200..800;1,200..800&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap'); 
    /* Hide the main header */
    header {visibility: hidden;}  
    /* Hide the menu button on the top right */
    .css-1v3fvcr {visibility: hidden;}
    /* Remove the spacing above the main content */
    .css-1d391kg {margin-top: 0 !important;}
    /* Add some margin and style to your title */
    .title {
        font-family: "Playfair Display", serif;
        font-size: 40px;
        font-weight: 900;
        color: black; /* Choose any color */
        margin-top: -150px;
        text-align: center;
    }
     .description {
        font-size: 24px;
      font-family: "Playfair Display", serif;
        color: #333;  /* Dark color for better readability */
        margin-top: -24px;
        font-weight: 500;  /* Light weight for a smooth look */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Your title as a custom HTML component
st.markdown(
    f'''
    <div class="title">
        <img src="data:image/jpg;base64,{image_base64}" alt="Logo" style="height:160px; vertical-align:middle; margin-right:2px;padding-top:10px">
        Air Quality Prediction Platform
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="description">Predict and analyze air quality for cities worldwide</div>', unsafe_allow_html=True)
# Main container
with st.container():
    # City selection and environmental inputs
    col1, col2 = st.columns([1, 2])

    with col1:
       
        selected_city = city_input(get_cities())
      

    with col2:
      
        temperature, humidity, wind_speed = environmental_inputs()
      
# Prediction section
if st.button("Predict Air Quality"):
    with st.spinner("Analyzing air quality..."):
        # Get prediction
        predicted_aqi = predictor.predict_aqi(
            selected_city, temperature, humidity, wind_speed, db
        )
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
    st.markdown("### AQI Levels & Colors")
    aqi_legend = """
        <style>
        .legend-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            width: 250px;
        }
        .legend-box {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            border-radius: 3px;
        }
        </style>
        <div class="legend-container">
            <div class="legend-item" style="background: #66bb6a;"><div class="legend-box" style="background: #66bb6a;"></div>Good (0-50)</div>
            <div class="legend-item" style="background: #ffeb3b;"><div class="legend-box" style="background: #ffeb3b;"></div>Moderate (51-100)</div>
            <div class="legend-item" style="background: #ffa726;"><div class="legend-box" style="background: #ffa726;"></div>Unhealthy for Sensitive Groups (101-150)</div>
            <div class="legend-item" style="background: #f44336;"><div class="legend-box" style="background: #f44336;"></div>Unhealthy (151-200)</div>
            <div class="legend-item" style="background: #9c27b0;"><div class="legend-box" style="background: #9c27b0;"></div>Very Unhealthy (201-300)</div>
            <div class="legend-item" style="background: #d32f2f;"><div class="legend-box" style="background: #d32f2f;"></div>Hazardous (301-500)</div>
        </div>
        """
    st.markdown(aqi_legend, unsafe_allow_html=True)
# Historical data section
st.markdown('<h3 id="HistoricalData">Historical Data</h3>', unsafe_allow_html=True)
historical_data = get_historical_data(selected_city, db)
st.plotly_chart(
    create_historical_chart(historical_data),
    use_container_width=True
)

# Data table
st.markdown("<h3 style=' font-size: 24px;'>View Historical Data Table</h3>", unsafe_allow_html=True)
with st.expander("Historical Data "):
        

# Example: Enhance your table with better fonts and custom styling
    st.markdown(
       """
        <style>
        /* Apply custom font */
        .dataframe-container {
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            width: 100%;
             color:black; /* Ensure table takes full width */
        }
        
        /* Styling for table header */
        .dataframe-container thead {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        /* Increase column width */
        .dataframe-container th, .dataframe-container td {
            padding: 10px;
            text-align: center;
            min-width: 150px;  /* Adjust column width */
            max-width: 250px;  /* Optional: Limit max width */
            word-wrap: break-word; /* Ensure text wraps properly */
        }

        /* Styling for table rows */
        .dataframe-container tbody tr:nth-child(odd) {
            background-color: #f9f9f9;
        }

        .dataframe-container tbody tr:nth-child(even) {
            background-color: #e9f7e9;
        }

        /* Hover effect on rows */
        .dataframe-container tbody tr:hover {
            background-color: #d3f8d3;
        }
        </style>
        """, unsafe_allow_html=True)


# Your DataFrame styling
    st.dataframe(
    historical_data.style.format({
        'aqi': '{:.1f}',
        'temperature': '{:.1f}',
        'humidity': '{:.1f}',
        'wind_speed': '{:.1f}'
        }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]},
        {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#f9f9f9')]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#e9f7e9')]},
        {'selector': 'tbody tr:hover', 'props': [('background-color', '#d3f8d3')]},
        {'selector': 'td', 'props': [('padding', '10px'), ('text-align', 'center')]},
         ])
            )
import os

# Team member data
import streamlit as st
import os

# Team member data
team_members = [
    {"name": "Shubham Gupta", "role": "Full Stack Java Developer", "bio": "Expert in backend development with Java", "image": "images/ShubhamProfile.jpg"},
    {"name": "Suhani Singh", "role": "Data Scientist", "bio": "Specialist in AI and Machine Learning for real-world applications.", "image": "images/suhani.jpg"},
    {"name": "Jatin Arora", "role": "Frontend Developer", "bio": "Passionate about crafting engaging UI/UX experiences.", "image": "images/jatin.jpg"},
    {"name": "Avyukt vashistha", "role": "Cloud Engineer", "bio": "Skilled in AWS, Azure, and DevOps tools.", "image": "images/AvyuktProfile.jpg"},
    {"name": "Nitish Kumar", "role": "Backend Developer", "bio": "Loves working on Backend and scalable applications.", "image": "images/nitish.jpg"},
    {"name": "Nandini Singh", "role": "Designer", "bio": "Driving product vision and user experience strategies.", "image": "images/nandiniSingh.jpg"},
    {"name": "Piyush kashyap", "role": "CyberSecurity", "bio": "Ensuring application security with best practices", "image": "images/piyushProfile.jpg"},
    {"name": "Kashish Chaudhary", "role": "Database Administrator", "bio": "Optimizing databases for high-performance applications.", "image": "images/kashish.jpg"}
]

# CSS for styling
st.markdown(
    """
    <style>
    .team-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        margin-bottom:30px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        color: black;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .team-card img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 10px;
        border: 3px solid white;
    }
    .team-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .team-role {
        font-size: 14px;
        font-style: italic;
        margin-bottom: 8px;
    }
    .team-bio {
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<h2 style='text-align: center;'>🚀 Meet Our Team</h2>", unsafe_allow_html=True)

# Function to check if an image exists
def encode_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    else:
        # Fallback image (Ensure "images/default.jpg" exists)
        with open("images/default.jpg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

# Render Team Cards in Rows of 3
cols_per_row = 3  # Number of cards per row
rows = [team_members[i:i + cols_per_row] for i in range(0, len(team_members), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for col, member in zip(cols, row):
        with col:
            image_base64 = encode_image(member['image'])
            st.markdown(
                f"""
                <div class="team-card" style="text-align: center; padding: 10px; border-radius: 10px; background: rgba(255, 255, 255, 0.2);">
                    <img src="data:image/jpeg;base64,{image_base64}" alt="{member['name']}" style="width: 100px; height: 100px; border-radius: 50%;">
                    <h3>{member['name']}</h3>
                    <p><strong>{member['role']}</strong></p>
                    <p>{member['bio']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )