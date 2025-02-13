from sqlalchemy import Column, Float, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from Base import Base

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.id'), nullable=False)
    temp = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    pressure = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    sea_level = Column(Integer, nullable=True)
    grnd_level = Column(Integer, nullable=True)
    visibility = Column(Integer, nullable=True)
    wind_speed = Column(Float, nullable=True)
    clouds = Column(Integer, nullable=True)
    sunrise = Column(Integer, nullable=False)
    sunset = Column(Integer, nullable=False)
    weather = Column(String, nullable=False)
    
    city = relationship("City", back_populates="weather_data")
