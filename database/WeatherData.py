# pylint: disable=invalid-name, too-few-public-methods
"""
This module defines the WeatherData model for the database. The WeatherData model
represents weather data for a specific city at a specific time.

Modules:
    sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
    datetime: Supplies classes for manipulating dates and times.
    uuid: Provides immutable UUID objects.
    Base: The declarative base class for the models.
"""

import uuid
from sqlalchemy import Column, Float, Integer, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Base import Base

class WeatherData(Base):
    """
    The WeatherData class represents weather data for a specific city at a specific time.

    Attributes:
        id (UUID): The unique identifier for the weather data entry.
        city_id (UUID): The unique identifier for the city.
        local_time (datetime): The local time of the weather data.
        temp (float): The temperature.
        feels_like (float): The perceived temperature.
        temp_min (float): The minimum temperature.
        temp_max (float): The maximum temperature.
        pressure (int): The atmospheric pressure.
        humidity (int): The humidity percentage.
        sea_level (int, optional): The sea level pressure.
        grnd_level (int, optional): The ground level pressure.
        visibility (int, optional): The visibility distance.
        wind_speed (float, optional): The wind speed.
        clouds (int, optional): The cloudiness percentage.
        sunrise (int): The sunrise time.
        sunset (int): The sunset time.
        weather (str): The weather description.
        city (relationship): The relationship to the City model.
    """
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
