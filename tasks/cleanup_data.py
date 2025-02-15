import uuid
import json
from prefect import task
from datetime import datetime

# @task
@task(cache_result_in_memory=False, persist_result=False)
def cleanup_weather_data(cityId: object, weather: object):
    """Task 1: Get or create the city"""

    if not cityId:
        return None
    
    if isinstance(weather, str):
        weather = json.loads(weather)

    try:
        return {
            'id': uuid.uuid4(),
            'city_id': cityId,
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


# @task
@task(cache_result_in_memory=False, persist_result=False)
def cleanup_city_obect(city: object):
    """Task 1: Get or create the city"""
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