# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hong-kong-travel-secret-key'
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or 'your-google-maps-api-key'
    CSV_DATA_PATH = os.environ.get('CSV_DATA_PATH') or 'Book.csv'