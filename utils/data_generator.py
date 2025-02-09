import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .database import AirQualityRecord, get_db
from sqlalchemy.orm import Session
from typing import List
from .cities_data import get_all_cities, get_region_and_state, get_city_size_factor

def generate_and_store_historical_data(city: str, db: Session) -> None:
    """Generate and store mock historical AQI data for a city"""
    np.random.seed(hash(city) % 100)

    # Adjust baseline AQI based on typical Indian city patterns
    base_aqi = {
        # North India
        'Delhi': 150, 'Gurugram': 140, 'Noida': 145, 'Chandigarh': 95,
        'Lucknow': 130, 'Kanpur': 135, 'Varanasi': 120, 'Patna': 125,
        'Jaipur': 110, 'Jodhpur': 100,

        # West India
        'Mumbai': 95, 'Pune': 85, 'Ahmedabad': 105, 'Surat': 90,
        'Nagpur': 80, 'Indore': 95, 'Bhopal': 90,

        # South India
        'Bangalore': 70, 'Chennai': 80, 'Hyderabad': 85, 'Kochi': 60,
        'Thiruvananthapuram': 55, 'Mysuru': 65, 'Coimbatore': 70,
        'Visakhapatnam': 75, 'Mangalore': 60,

        # East India
        'Kolkata': 110, 'Bhubaneswar': 85, 'Guwahati': 80,
        'Shillong': 60, 'Gangtok': 55, 'Imphal': 65
    }

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

    # Calculate base AQI for this city
    if city not in base_aqi:
        base_aqi_value = 80  # Default value
        base_aqi_value *= region_factor
        base_aqi_value *= size_factor
    else:
        base_aqi_value = base_aqi[city]

    # Generate 30 days of data
    for i in range(30):
        date = datetime.now() - timedelta(days=30-i)

        # Add seasonal and daily variations
        season_factor = 1.2 if date.month in [11, 12, 1] else 0.8  # Higher in winter

        # Convert numpy values to Python native types
        aqi = float(np.clip(np.random.normal(loc=base_aqi_value, scale=30) * season_factor, 0, 500))
        temperature = float(np.random.normal(30, 5))  # Typical Indian temperatures
        humidity = float(np.random.normal(65, 15))
        wind_speed = float(np.random.normal(12, 4))

        record = AirQualityRecord(
            city=city,
            date=date,
            aqi=aqi,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            is_prediction=0
        )
        db.add(record)

    db.commit()

def get_historical_data(city: str, db: Session) -> pd.DataFrame:
    """Get historical data for a city from database"""
    records = (db.query(AirQualityRecord)
              .filter(AirQualityRecord.city == city)
              .filter(AirQualityRecord.is_prediction == 0)
              .order_by(AirQualityRecord.date)
              .all())

    if not records:
        # Generate data if none exists
        generate_and_store_historical_data(city, db)
        records = (db.query(AirQualityRecord)
                  .filter(AirQualityRecord.city == city)
                  .filter(AirQualityRecord.is_prediction == 0)
                  .order_by(AirQualityRecord.date)
                  .all())

    return pd.DataFrame([{
        'date': r.date,
        'aqi': r.aqi,
        'temperature': r.temperature,
        'humidity': r.humidity,
        'wind_speed': r.wind_speed
    } for r in records])

def get_cities() -> List[str]:
    """Return a list of major Indian cities grouped by region"""
    return get_all_cities()