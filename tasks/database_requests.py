from prefect import task
from sqlalchemy import text

def generate_city_cache_key(context, parameters):
    # parameters will be a dict containing the task arguments
    city = parameters['city'] 
    return f"{city['city']},{city['state']},{city['country']}"

def generate_weather_cache_key(context, parameters):
    # parameters will be a dict containing the task arguments
    weather = parameters['weather'] 
    return f"{weather['id']}"

# @task(cache_key_fn=generate_city_cache_key)
@task(cache_result_in_memory=False, persist_result=False)
def get_or_create_city_id(city: object, engine: object):
    """Task 1: Get or create the city"""
    with engine.connect() as connection:
      query = f"SELECT * FROM city WHERE city = :city AND state = :state AND country = :country"
    
      result = connection.execute(text(query), {"city": city['city'], "state": city['state'], "country": city['country']}).fetchone()
      
      if result:
        return result[0]
      else:
        query = f"INSERT INTO city (id, city, state, country, lat, lon) VALUES (:id, :city, :state, :country, :lat, :lon) RETURNING id"
        result = connection.execute(text(query), city).fetchone()
        connection.commit()
        return result[0]
      
# @task(cache_key_fn=generate_weather_cache_key)
@task(cache_result_in_memory=False, persist_result=False)
def insert_weather_data(weather: object, engine: object):
    """Task 2: Insert the weather data"""
    print(weather)
    with engine.connect() as connection:
      query = f"INSERT INTO weather_data (id, city_id, local_time, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, sea_level, grnd_level, weather, clouds, sunrise, sunset) VALUES (:id, :cityId, :local_time, :temp, :feels_like, :temp_min, :temp_max, :pressure, :humidity, :visibility, :wind_speed, :sea_level, :grnd_level, :weather, :clouds, :sunrise, :sunset)"
      connection.execute(text(query), weather)
      connection.commit()
      return weather