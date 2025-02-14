import uuid
import json
from prefect import task
from datetime import datetime

@task
def cleanup_weather_data(cityId: object, weather: object):
    """Task 1: Get or create the city"""
    
    if isinstance(weather, str):
        weather = json.loads(weather)

    return {
        'id': uuid.uuid4(),
        'cityId': cityId,
        'local_time': datetime.now(),
        'temp': weather['main']['temp'],
        'feels_like': weather['main']['feels_like'],
        'temp_min': weather['main']['temp_min'],
        'temp_max': weather['main']['temp_max'],
        'pressure': weather['main']['pressure'],
        'humidity': weather['main']['humidity'],
        'visibility': weather['visibility'],
        'wind_speed': weather['wind']['speed'],
        'sea_level': weather['main']['sea_level'],
        'grnd_level': weather['main']['grnd_level'],
        'weather': weather['weather'][0]['description'],
        'clouds': weather['clouds']['all'],
        'sunrise': weather['sys']['sunrise'],
        'sunset': weather['sys']['sunset'],
    }


@task
def cleanup_city_obect(city: object):
    """Task 1: Get or create the city"""
    return {
        'id': uuid.uuid4(),
        'city': city['name'],
        'state': city['state'],
        'country': city['country'],
        'lat': city['lat'],
        'lon': city['lon']
    }