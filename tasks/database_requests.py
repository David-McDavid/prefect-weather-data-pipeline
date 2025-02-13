import uuid
from prefect import task
from sqlalchemy import text

def generate_city_cache_key(context, parameters):
    # parameters will be a dict containing the task arguments
    city = parameters['city'] 
    return f"{city['city']},{city['state']},{city['country']}"

@task(cache_key_fn=generate_city_cache_key)
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
        return result