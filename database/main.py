"""
This module initializes the database by creating all the necessary tables.
It loads the database URL from the environment variables and uses SQLAlchemy
to create the database engine and tables.

Modules:
    os: Provides a way of using operating system dependent functionality.
    sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
    dotenv: Reads key-value pairs from a .env file and can set them as environment variables.
    City: Defines the City model.
    WeatherData: Defines the WeatherData model.
    Base: The declarative base class for the models.
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from Base import Base

load_dotenv()

if __name__ == "__main__":
    dbUrl = os.getenv("DB_URL")
    engine = create_engine(dbUrl)
    Base.metadata.create_all(engine)
