import httpx
from prefect import task

@task
def fetch_weather(location: object, api_key: str):
    """Task 1: Fetch the weather for a city"""
    return httpx.get(f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}").text

@task
def fetch_location(city: object, api_key: str):
    """Task 1: Fetch the location for a city"""
    return httpx.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city['city']},{city['state']},{city['countryCode']}&limit=5&appid={api_key}").json()