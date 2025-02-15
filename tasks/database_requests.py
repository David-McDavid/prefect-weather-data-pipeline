import json
from prefect import task
from sqlalchemy import text
from uuid import UUID
from datetime import datetime

def generate_city_cache_key(context, parameters):
    # parameters will be a dict containing the task arguments
    city = parameters['city'] 
    return f"{city['city']},{city['state']},{city['country']}"

# @task(cache_key_fn=generate_city_cache_key)
@task(cache_result_in_memory=False, persist_result=False)
def get_or_create_city_id(city: object, engine: object):
    """Task 1: Get or create the city"""
    with engine.connect() as connection:
      query = f"SELECT * FROM city WHERE city = :city AND state = :state AND country = :country"
    
      result = connection.execute(text(query), {"city": city['city'], "state": city['state'], "country": city['country']}).fetchone()
      
      if not result:
        query = f"INSERT INTO city (id, city, state, country, lat, lon) VALUES (:id, :city, :state, :country, :lat, :lon) RETURNING id"
        result = connection.execute(text(query), city).fetchone()
      
      connection.commit()
      return result[0]
    
@task(cache_result_in_memory=False, persist_result=False)
def insert_weather_data_bulk(cleaned_weather_data, engine):
    # todo remove json dump
    def convert_uuid(obj):
        if isinstance(obj, UUID):
            return str(obj)
        
        if isinstance(obj, datetime):
            return obj.__str__()
        
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with open('data.json', 'w') as file:
        json.dump(cleaned_weather_data, file, indent=4, default=convert_uuid)

    with engine.connect() as connection:
        connection.execute(
            text("""
                INSERT INTO weather_data (
                    id, city_id, local_time, temp, feels_like, temp_min, temp_max, pressure, humidity, 
                    visibility, wind_speed, sea_level, grnd_level, weather, clouds, sunrise, sunset
                ) VALUES (
                    :id, :city_id, :local_time, :temp, :feels_like, :temp_min, :temp_max, :pressure, :humidity, 
                    :visibility, :wind_speed, :sea_level, :grnd_level, :weather, :clouds, :sunrise, :sunset
                )
            """),
            cleaned_weather_data
        )
        connection.commit()