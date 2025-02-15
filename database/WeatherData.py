from sqlalchemy import Column, Float, Integer, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from Base import Base

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.id'), nullable=False)
    local_time = Column(DateTime(timezone=True), nullable=False)
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    sea_level = Column(Integer, nullable=True)
    grnd_level = Column(Integer, nullable=True)
    visibility = Column(Integer, nullable=True)
    wind_speed = Column(Float, nullable=True)
    clouds = Column(Integer, nullable=True)
    sunrise = Column(Integer)
    sunset = Column(Integer)
    weather = Column(String, nullable=False)
    
    city = relationship("City", back_populates="weather_data")