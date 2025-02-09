import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_historical_data(city):
    """Generate mock historical AQI data for a city"""
    np.random.seed(hash(city) % 100)
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=30),
        end=datetime.now(),
        freq='D'
    )
    
    aqi_values = np.random.normal(loc=80, scale=20, size=len(dates))
    aqi_values = np.clip(aqi_values, 0, 300)
    
    return pd.DataFrame({
        'date': dates,
        'aqi': aqi_values,
        'temperature': np.random.normal(25, 5, len(dates)),
        'humidity': np.random.normal(60, 10, len(dates)),
        'wind_speed': np.random.normal(15, 5, len(dates))
    })

def get_cities():
    """Return a list of sample cities"""
    return [
        "New York", "London", "Tokyo", "Paris", "Beijing",
        "Mumbai", "Singapore", "Sydney", "Dubai", "Moscow"
    ]
