"""
This module contains tasks for cleaning up city and weather data.

Functions:
    - cleanup_weather_data: Task to clean up weather data for a city.
    - cleanup_city_obect: Task to clean up city data.
"""

import uuid
import json
from datetime import datetime
from prefect import task

@task(cache_result_in_memory=False, persist_result=False)
def cleanup_weather_data(city_id: object, weather: object):
    """
    Task to clean up weather data for a city.

    Args:
        city_id (object): The ID of the city.
        weather (object): A dictionary or JSON string containing weather data.

    Returns:
        dict: A dictionary containing cleaned weather data.
    """
    if isinstance(weather, str):
        weather = json.loads(weather)

    try:
        return {
            'id': uuid.uuid4(),
            'city_id': city_id,
            'local_time': datetime.now(),
            'temp': weather.get('main', {}).get('temp'),
            'feels_like': weather.get('main', {}).get('feels_like'),
            'temp_min': weather.get('main', {}).get('temp_min'),
            'temp_max': weather.get('main', {}).get('temp_max'),
            'pressure': weather.get('main', {}).get('pressure'),
            'humidity': weather.get('main', {}).get('humidity'),
            'visibility': weather.get('visibility'),
            'wind_speed': weather.get('wind', {}).get('speed'),
            'sea_level': weather.get('main', {}).get('sea_level'),
            'grnd_level': weather.get('main', {}).get('grnd_level'),
            'weather': weather.get('weather', [{}])[0].get('description'),
            'clouds': weather.get('clouds', {}).get('all'),
            'sunrise': weather.get('sys', {}).get('sunrise'),
            'sunset': weather.get('sys', {}).get('sunset'),
        }
    except Exception as e:
        print('error: ', e)
        print('weather: ', weather)
        raise e

@task(cache_result_in_memory=False, persist_result=False)
def cleanup_city_obect(city: object):
    """
    Task to clean up city data.

    Args:
        city (object): A dictionary containing city information.

    Returns:
        dict: A dictionary containing cleaned city data.
    """
    try:
        return {
            'id': uuid.uuid4(),
            'city': city['name'],
            'state': city.get('state'),
            'country': city['country'],
            'lat': city['lat'],
            'lon': city['lon']
        }
    except Exception as e:
        print('error: ', e)
        print('city: ', city)
        raise e
