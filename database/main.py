import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from City import City
from WeatherData import WeatherData
from Base import Base

load_dotenv()

if __name__ == "__main__":
    dbUrl = os.getenv("DATABASE_URL")
    engine = create_engine(dbUrl)
    Base.metadata.create_all(engine)
