# pylint: disable=invalid-name, too-few-public-methods
"""
This module defines the City model for the database. The City model represents
a city with its geographical coordinates and related weather data.
"""

import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Base import Base

class City(Base):
    """
    The City class represents a city in the database.

    Attributes:
        id (UUID): The unique identifier for the city.
        city (str): The name of the city.
        state (str): The state where the city is located.
        country (str): The country where the city is located.
        lat (float): The latitude of the city.
        lon (float): The longitude of the city.
        weather_data (relationship): The relationship to the WeatherData model.
    """
    __tablename__ = 'city'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String, nullable=False)
    state = Column(String)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    weather_data = relationship("WeatherData", back_populates="city")
