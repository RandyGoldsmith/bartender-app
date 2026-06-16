from fastapi import FastAPI
import psycopg2

conn = psycopg2.connect(
    dbname="bartender_app",
    user="randolphgoldsmith",
    password="",
    host="localhost",
    port="5432"
)

db = conn.cursor()

app = FastAPI()

@app.get("/drinks")
def get_drinks():
    db.execute("SELECT drink_id, name, glass_type, instructions FROM drinks")
    rows = db.fetchall()
    return [
        {"drink_id": row[0], "name": row[1], "glass_type": row[2], "instructions": row[3]}
        for row in rows
    ]


@app.get("/drinks/flavor/{flavor}")
def get_flavor(flavor):
    query = """
        SELECT drinks.name, flavor_profiles.name AS flavor
        FROM drinks
        JOIN drink_flavors ON drinks.drink_id = drink_flavors.drink_id
        JOIN flavor_profiles ON drink_flavors.flavor_id = flavor_profiles.flavor_id
        WHERE flavor_profiles.name = %s
    """
    db.execute(query, (flavor,))
    rows = db.fetchall()
    return [
        {
            "name": row[0],
            "flavor": row[1]
        }
        for row in rows
    ]

@app.get("/drinks/ingredient/{ingredient}")
def get_ingredient(ingredient):
    query = """
        SELECT drinks.name, ingredients.name, drink_ingredients.amount
        FROM drinks
        JOIN drink_ingredients ON drink_ingredients.drink_id = drinks.drink_id
        JOIN ingredients ON ingredients.ingredient_id = drink_ingredients.ingredient_id
        WHERE ingredients.name = %s
    """
    db.execute(query, (ingredient,))
    rows = db.fetchall()
    return [{
        "name": row[0],
        "ingredient": row[1],
        "amount": row[2]
    }
     for row in rows
    ]

@app.get("/drinks/{drink_name}")
def get_drink_name(drink_name):
    query = """
    SELECT drinks.name, drinks.glass_type, drinks.instructions, ingredients.name, drink_ingredients.amount, flavor_profiles.name
    FROM drinks
    JOIN drink_ingredients ON drink_ingredients.drink_id = drinks.drink_id
    JOIN ingredients ON ingredients.ingredient_id = drink_ingredients.ingredient_id
    JOIN drink_flavors ON drink_flavors.drink_id = drinks.drink_id
    JOIN flavor_profiles ON flavor_profiles.flavor_id = drink_flavors.flavor_id
    WHERE drinks.name = %s

"""
    db.execute(query, (drink_name,))
    rows = db.fetchall()
    return [{
        "name": row[0],
        "glass_type": row[1],
        "instructions": row[2],
        "ingredient": row[3],
        "amount": row[4],
        "flavor": row[5]
    }
    for row in rows
    ]
