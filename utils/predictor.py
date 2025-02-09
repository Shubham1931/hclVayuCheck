import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from .database import AirQualityRecord
from .cities_data import get_region_and_state, get_city_size_factor

class AQIPredictor:
    def __init__(self):
        self.model = LinearRegression()
        # City-specific pollution factors
        self.city_factors = {
            # North India (generally higher pollution levels)
            'Delhi': 1.5, 'Gurugram': 1.45, 'Noida': 1.45, 'Chandigarh': 1.1,
            'Lucknow': 1.3, 'Kanpur': 1.35, 'Varanasi': 1.25, 'Patna': 1.3,
            'Jaipur': 1.2, 'Jodhpur': 1.15,

            # West India (moderate pollution levels)
            'Mumbai': 1.2, 'Pune': 0.95, 'Ahmedabad': 1.1, 'Surat': 1.0,
            'Nagpur': 0.9, 'Indore': 1.05, 'Bhopal': 1.0,

            # South India (generally lower pollution levels)
            'Bangalore': 0.9, 'Chennai': 1.0, 'Hyderabad': 0.95, 'Kochi': 0.7,
            'Thiruvananthapuram': 0.65, 'Mysuru': 0.75, 'Coimbatore': 0.8,
            'Visakhapatnam': 0.85, 'Mangalore': 0.7,

            # East India (varied pollution levels)
            'Kolkata': 1.3, 'Bhubaneswar': 0.95, 'Guwahati': 0.9,
            'Shillong': 0.7, 'Gangtok': 0.65, 'Imphal': 0.75
        }

    def get_aqi_level(self, aqi):
        """Return AQI level and color based on Indian AQI standards"""
        if aqi <= 50:
            return "Good", "#4CAF50"
        elif aqi <= 100:
            return "Satisfactory", "#90EE90"
        elif aqi <= 200:
            return "Moderate", "#FFC107"
        elif aqi <= 300:
            return "Poor", "#FF9800"
        elif aqi <= 400:
            return "Very Poor", "#FF5722"
        else:
            return "Severe", "#9C27B0"

    def predict_aqi(self, city, temperature, humidity, wind_speed, db):
        """Predict AQI based on Indian city characteristics"""
        # Get city-specific factor
        city_factor = self.city_factors.get(city, 1.0)

        # Get region and state-based factors
        region, state = get_region_and_state(city)
        region_factors = {
            "North": 1.2,  # Higher pollution in North India
            "South": 0.8,  # Lower pollution in South India
            "East": 1.0,   # Moderate pollution in East India
            "West": 1.1,   # Slightly higher pollution in West India
            "Northeast": 0.7  # Lower pollution in Northeast India
        }
        region_factor = region_factors.get(region, 1.0)

        # Get city size factor
        size_factor = get_city_size_factor(city)

        # Calculate combined factor
        if city not in self.city_factors:
            city_factor = region_factor * size_factor

        # Season factor (higher in winter months)
        current_month = datetime.now().month
        season_factor = 1.3 if current_month in [11, 12, 1] else 1.0

        # Calculate base AQI
        predicted_aqi = float(
            temperature * 2.0 +  # Higher impact of temperature
            humidity * 0.8 +     # Moderate impact of humidity
            wind_speed * (-1.5) + # Strong negative impact of wind
            np.random.normal(0, 5)  # Add some randomness
        )

        # Apply city and season factors
        predicted_aqi = predicted_aqi * city_factor * season_factor

        # Clip to valid AQI range for India (0-500)
        predicted_aqi = float(max(0, min(500, predicted_aqi)))

        # Store prediction
        record = AirQualityRecord(
            city=city,
            date=datetime.utcnow(),
            aqi=predicted_aqi,
            temperature=float(temperature),
            humidity=float(humidity),
            wind_speed=float(wind_speed),
            is_prediction=1
        )
        db.add(record)
        db.commit()

        return predicted_aqi