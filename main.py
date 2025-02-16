"""
This module contains the main flow for processing city weather data.

It includes tasks for fetching, cleaning, and inserting weather data into the database.

The main flow processes a list of cities, retrieves their
weather data, cleans it, and stores it in the database.

Functions:
    - process_city: Task to process a single city to fetch and clean weather data.
    - show_cities: Flow to process a list of cities and insert their weather data into the database.
"""

import os
import json
from dotenv import load_dotenv
from prefect import flow, task
from sqlalchemy import create_engine
from tasks.open_weather_requests import fetch_weather, fetch_location
from tasks.database_requests import get_or_create_city_id, insert_weather_data_bulk
from tasks.cleanup_data import cleanup_city_obect, cleanup_weather_data
# from prefect.task_runners import ThreadPoolTaskRunner

load_dotenv()
api_key = os.getenv("OPEN_WEATHER_API_KEY")
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

@task(cache_result_in_memory=False, persist_result=False)
def process_city(city: object):
    """
    Task: Process a city to fetch and clean weather data.

    Args:
        city (object): A dictionary containing city information.

    Returns:
        dict: A dictionary containing cleaned weather data, or None if any step fails.
    """
    location = fetch_location(city, api_key)
    if location is None:
        return None

    weather = fetch_weather(location, api_key)
    if weather is None:
        return None

    cleaned_city_object = cleanup_city_obect(location)
    city_id = get_or_create_city_id(cleaned_city_object, engine)
    if not city_id:
        return None

    cleaned_weather_object = cleanup_weather_data(city_id, weather)

    return cleaned_weather_object


# If you want to use SQLite, you can use the following flow decorator instead.
# @flow(log_prints=True, task_runner=ThreadPoolTaskRunner(max_workers=1))
@flow(log_prints=True)
def show_cities(cities: list[object]):
    """
    Flow: Show the cities and insert their weather data into the database.

    Args:
        cities (list[object]): A list of dictionaries containing city information.

    Returns:
        list: A list of results from processing each city.
    """
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
    with open("./assets/cities.json", "r", encoding="utf-8") as file:
        city_list = json.load(file)['cities']
        show_cities(city_list)
