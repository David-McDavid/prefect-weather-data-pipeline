
import os
import json
from dotenv import load_dotenv
from prefect import flow, task
from sqlalchemy import create_engine, text
from tasks.open_weather_requests import fetch_weather, fetch_location
from tasks.database_requests import get_or_create_city_id, insert_weather_data
from tasks.cleanup_data import cleanup_city_obect, cleanup_weather_data

load_dotenv()
api_key = os.getenv("OPEN_WEATHER_API_KEY")
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

cities = [
  {"city": "Anchorage", "state": "Alaska", "countryCode": "USA"},
  {"city": "Nashville", "state": "Tennessee", "countryCode": "USA"}
]

@flow(log_prints=True)
def show_cities(cities: list[object]):
    """Flow: Show the cities"""
    for city in cities:
        location = fetch_location(city, api_key)
        weather = fetch_weather(location, api_key)
        cleanedCityObject = cleanup_city_obect(location)
        cityId = get_or_create_city_id(cleanedCityObject, engine)
        cleanedWeatherData = cleanup_weather_data(cityId, weather)
        insert_weather_data(cleanedWeatherData, engine)
      


if __name__ == "__main__":
    show_cities(cities)
    # with open("./assets/cities.json", "r") as file:
    #   cities = json.load(file)['cities']