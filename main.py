import psycopg2
from countryinfo import CountryInfo
from dotenv import load_dotenv
import os

load_dotenv()
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# connection = psycopg2.connect(
#     host=POSTGRES_HOST,
#     port=POSTGRES_PORT,
#     database=POSTGRES_DB,
#     user=POSTGRES_USER,
#     password=POSTGRES_PASSWORD,
#
#


POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

connection = psycopg2.connect(POSTGRES_URL)
cursor = connection.cursor()
cursor.execute("""
--drop table if exists countries;
    create table if not exists countries(
        id serial primary key ,
        name varchar(50) unique,
        area integer,
        capital varchar(100),
        population integer,
        languages text[]
);
""")
connection.commit()

while True:
    country = input("country: ").lower()
    if country == "stop":
        break

    data = CountryInfo(country).info()
    name = data.get("name")
    area = data.get("area")
    capital = data.get("capital")
    population = data.get("population")
    languages = data.get("languages")

    cursor.execute("""
    insert into countries(name, area, capital, population, languages)
    values (%(name)s, %(area)s, %(capital)s, %(population)s, %(languages)s) 
    on conflict(name) do update set 
                                area = %(area)s,
                                capital = %(capital)s,
                                population = %(population)s,
                                languages = %(languages)s;
    """, {
        "name": name,
        "area": area,
        "capital": capital,
        "population": population,
        "languages": languages,
    })

    connection.commit()
    print("country added")
