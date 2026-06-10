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
