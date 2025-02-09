import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from .database import AirQualityRecord

class AQIPredictor:
    def __init__(self):
        self.model = LinearRegression()
        # City-specific pollution factors
        self.city_factors = {
            'Delhi': 1.5,
            'Mumbai': 1.2,
            'Bangalore': 0.9,
            'Chennai': 1.0,
            'Kolkata': 1.3,
            'Hyderabad': 0.95,
            'Pune': 0.85,
            'Ahmedabad': 1.1,
            'Jaipur': 1.2,
            'Lucknow': 1.3
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