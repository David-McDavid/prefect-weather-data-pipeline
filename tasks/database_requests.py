"""
This module contains tasks for interacting with the database, specifically for
retrieving or creating city IDs and inserting weather data in bulk.
"""

from prefect import task
from queries.queries import get_city_query, insert_city_query, bulk_insert_weather_query

# def generate_city_cache_key(context, parameters):
#     # parameters will be a dict containing the task arguments
#     city = parameters['city']
#     return f"{city['city']},{city['state']},{city['country']}"

# @task(cache_key_fn=generate_city_cache_key)
@task(cache_result_in_memory=False, persist_result=False)
def get_or_create_city_id(city: object, engine: object):
    """
    Retrieve or create a city ID in the database.

    Args:
        city (object): A dictionary containing city information with keys 'city', 
                       state', and 'country'.
        engine (object): A SQLAlchemy engine object for database connection.

    Returns:
        int: The ID of the city.
    """
    with engine.connect() as connection:
        result = connection.execute(get_city_query, city).fetchone()

        if not result:
            result = connection.execute(insert_city_query, city).fetchone()

        connection.commit()
        return result[0]

@task(cache_result_in_memory=False, persist_result=False)
def insert_weather_data_bulk(cleaned_weather_data, engine):
    """
    Insert cleaned weather data into the database in bulk.

    Args:
        cleaned_weather_data (list): A list of dictionaries containing cleaned weather data.
        engine (object): A SQLAlchemy engine object for database connection.
    """
    with engine.connect() as connection:
        connection.execute(bulk_insert_weather_query, cleaned_weather_data)
        connection.commit()
