"""
This module contains SQL queries used for interacting with the database.

Queries:
    - get_city_query: Retrieves a city record based on city name, state, and country.
    - insert_city_query: Inserts a new city record into the city table and returns the city ID.
    - bulk_insert_weather_query: Inserts multiple weather data records into the weather_data table.
"""

from sqlalchemy import text

get_city_query = text("""
SELECT * 
FROM city 
WHERE city = :city 
AND (state = :state OR :state IS NULL) 
AND country = :country
""")

insert_city_query = text("""
INSERT INTO city (id, city, state, country, lat, lon)
VALUES (:id, :city, :state, :country, :lat, :lon)
RETURNING id
""")

bulk_insert_weather_query = text("""
INSERT INTO weather_data (
    id, city_id, local_time, temp, feels_like, temp_min, temp_max, pressure, humidity, 
    visibility, wind_speed, sea_level, grnd_level, weather, clouds, sunrise, sunset
) VALUES (
    :id, :city_id, :local_time, :temp, :feels_like, :temp_min, :temp_max, :pressure, :humidity, 
    :visibility, :wind_speed, :sea_level, :grnd_level, :weather, :clouds, :sunrise, :sunset
)
""")
