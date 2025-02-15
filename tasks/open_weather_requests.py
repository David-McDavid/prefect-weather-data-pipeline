import httpx
from prefect import task

# @task
@task(cache_result_in_memory=False, persist_result=False)
def fetch_weather(location: object, api_key: str):
    """Task 1: Fetch the weather for a city"""
    return httpx.get(f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}").text

# @task
@task(cache_result_in_memory=False, persist_result=False)
def fetch_location(city: object, api_key: str):
    """Task 1: Fetch the location for a city"""
    try:
        record = httpx.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city['city']},{city['state']},{city['countryCode']}&limit=5&appid={api_key}").json()
        return record[0] if record else None
    except Exception as e:
        print('error: ', e)
        print('city: ', city)
        raise e