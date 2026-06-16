import requests
import psycopg2

conn = psycopg2.connect(
    dbname="bartender_app",
    user="randolphgoldsmith",
    password="",
    host="localhost",
    port="5432"
)
db = conn.cursor()

def seed_drinks():
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a")
    data = response.json()
    drinks = data["drinks"]

    for drink in drinks:
        print(drink["strDrink"])


seed_drinks()