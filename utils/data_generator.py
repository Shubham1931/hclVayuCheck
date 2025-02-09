import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .database import AirQualityRecord, get_db
from sqlalchemy.orm import Session
from typing import List

def generate_and_store_historical_data(city: str, db: Session) -> None:
    """Generate and store mock historical AQI data for a city"""
    np.random.seed(hash(city) % 100)

    # Generate 30 days of data
    for i in range(30):
        date = datetime.now() - timedelta(days=30-i)

        # Convert numpy values to Python native types
        aqi = float(np.clip(np.random.normal(loc=80, scale=20), 0, 300))
        temperature = float(np.random.normal(25, 5))
        humidity = float(np.random.normal(60, 10))
        wind_speed = float(np.random.normal(15, 5))

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
    """Return a list of sample cities"""
    return [
        "New York", "London", "Tokyo", "Paris", "Beijing",
        "Mumbai", "Singapore", "Sydney", "Dubai", "Moscow"
    ]