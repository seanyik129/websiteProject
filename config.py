# 配置文件
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hong-kong-travel-secret-key'
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or 'your-google-maps-api-key'
    # 使用绝对路径或明确的相对路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database/travel_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False