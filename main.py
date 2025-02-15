
import os
import json
from dotenv import load_dotenv
from prefect import flow, task
from sqlalchemy import create_engine, text
from tasks.open_weather_requests import fetch_weather, fetch_location
from tasks.database_requests import get_or_create_city_id, insert_weather_data_bulk
from tasks.cleanup_data import cleanup_city_obect, cleanup_weather_data
from prefect.task_runners import ThreadPoolTaskRunner

load_dotenv()
api_key = os.getenv("OPEN_WEATHER_API_KEY")
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)


@task(cache_result_in_memory=False, persist_result=False)
def process_city(city: object):
    location = fetch_location(city, api_key)
    if location is None:
        return None
    
    weather = fetch_weather(location, api_key)
    if weather is None:
        return None
    
    cleanedCityObject = cleanup_city_obect(location)
    cityId = get_or_create_city_id(cleanedCityObject, engine)
    if not cityId:
        return None
    
    cleanedWeatherObject = cleanup_weather_data(cityId, weather)

    if 'city_id' not in cleanedWeatherObject:
        return None
    
    return cleanedWeatherObject

@flow(log_prints=True, task_runner=ThreadPoolTaskRunner(max_workers=1))
def show_cities(cities: list[object]):
    """Flow: Show the cities"""
    futures = []
    for city in cities:
        future = process_city.submit(city)
        futures.append(future)

    results = [future.result() for future in futures]
    cleaned_weather_data = [result for result in results if result is not None]

    if cleaned_weather_data:
        insert_weather_data_bulk(cleaned_weather_data, engine)

    return results
      
if __name__ == "__main__":
    with open("./assets/cities.json", "r") as file:
      cities = json.load(file)['cities']
      show_cities(cities)