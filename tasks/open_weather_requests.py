"""
This module contains tasks for fetching weather and location data from the OpenWeather API.
"""

import httpx
from prefect import task

@task(cache_result_in_memory=False, persist_result=False)
def fetch_weather(location: object, api_key: str):
    """
    Fetch the weather for a given location.

    Args:
        location (object): A dictionary containing the latitude and longitude of the location.
        api_key (str): The API key for accessing the OpenWeather API.

    Returns:
        str: The weather data in JSON format as a string.
    """
    lat, lon = location['lat'], location['lon']
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    return httpx.get(url).text

@task(cache_result_in_memory=False, persist_result=False)
def fetch_location(city: object, api_key: str):
    """
    Fetch the geographical coordinates for a given city.

    Args:
        city (object): A dictionary containing the city name, state, and country code.
        api_key (str): The API key for accessing the OpenWeather API.

    Returns:
        dict: A dictionary containing the geographic coordinates of the city, or None if not found.
    """
    try:
        city_name, state, country_code = city['city'], city['state'], city['countryCode']
        q_string = f"{city_name},{state},{country_code}"
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={q_string}&appid={api_key}"
        record = httpx.get(url).json()
        return record[0] if record else None
    except Exception as e:
        print('error: ', e)
        print('city: ', city)
        raise e
