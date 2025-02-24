from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class AirQualityRecord(Base):
    """Model for storing air quality measurements and predictions"""
    __tablename__ = "air_quality_records"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    aqi = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    is_prediction = Column(Integer, default=0)  # 0 for historical, 1 for prediction

    @classmethod
    def create_tables(cls):
        """Create all database tables"""
        Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
AirQualityRecord.create_tables()
