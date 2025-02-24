import os
import csv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Fix potential incorrect PostgreSQL URL format
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Extract data from 'air_quality_records'
try:
    result = session.execute(text("SELECT * FROM air_quality_records;"))  # ✅ FIXED
    records = result.fetchall()

    # Print extracted data
    print("Extracted Data:")
    for row in records:
        print(row)

    # Save data to CSV
    csv_filename = "air_quality_data.csv"
    with open(csv_filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(result.keys())  # Column headers
        writer.writerows(records)

    print(f"Data successfully saved to {csv_filename}")

except Exception as e:
    print("Error extracting data:", e)

finally:
    session.close()
