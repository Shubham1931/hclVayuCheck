import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from .database import AirQualityRecord

class AQIPredictor:
    def __init__(self):
        self.model = LinearRegression()

    def get_aqi_level(self, aqi):
        """Return AQI level and color based on value"""
        if aqi <= 50:
            return "Good", "#4CAF50"
        elif aqi <= 100:
            return "Moderate", "#FFC107"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups", "#FF9800"
        elif aqi <= 200:
            return "Unhealthy", "#FF5722"
        elif aqi <= 300:
            return "Very Unhealthy", "#9C27B0"
        else:
            return "Hazardous", "#FF0000"

    def predict_aqi(self, city, temperature, humidity, wind_speed, db):
        """Predict AQI and store in database"""
        # Simple weighted calculation for demonstration
        predicted_aqi = float(
            temperature * 1.5 +
            humidity * 0.8 +
            wind_speed * (-0.5) +
            np.random.normal(0, 5)  # Add some randomness
        )
        predicted_aqi = float(max(0, min(300, predicted_aqi)))  # Clip between 0 and 300

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