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

    flavor_map = {
            "lemon juice": "sour",
            "lime juice": "sour",
            "orange juice": "sweet",
            "grenadine": "sweet",
            "simple syrup": "sweet",
            "sugar": "sweet",
            "campari": "bitter",
            "angostura bitters": "bitter",
            "tabasco": "spicy",
            "ginger beer": "spicy"
        }
    
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a")
    data = response.json()
    drinks = data["drinks"]

    for drink in drinks:
        name = drink["strDrink"]
        glass = drink["strGlass"]
        instructions = drink["strInstructions"]
        
        db.execute(
            "INSERT INTO drinks (name, glass_type, instructions) VALUES (%s, %s, %s) RETURNING drink_id",
            (name, glass, instructions)
        )

        drink_id = db.fetchone()[0]
        
        for i in range(1, 16):
            ingredient = drink[f"strIngredient{i}"]
            amount = drink[f"strMeasure{i}"]

            if ingredient is None:
                break

            db.execute(
                "INSERT INTO ingredients (name) VALUES (%s) RETURNING ingredient_id",
                (ingredient,)
            )
            ingredient_id = db.fetchone()[0]

            db.execute(
                "INSERT INTO drink_ingredients (drink_id, ingredient_id, amount) VALUES (%s, %s, %s)",
                (drink_id, ingredient_id, amount)
            )


        

        flavors_added = set()

        for i in range(1, 16):
            ingredient = drink[f"strIngredient{i}"]
            if ingredient is None:
                break
    
            ingredient_lower = ingredient.lower()
            if ingredient_lower in flavor_map:
                flavor_name = flavor_map[ingredient_lower]
        
                if flavor_name not in flavors_added:
                    db.execute(
                        "INSERT INTO flavor_profiles (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING flavor_id",
                        (flavor_name,)
                    )
                    result = db.fetchone()
                    if result:
                        flavor_id = result[0]
                    else:
                        db.execute("SELECT flavor_id FROM flavor_profiles WHERE name = %s", (flavor_name,))
                        flavor_id = db.fetchone()[0]
            
                    db.execute(
                        "INSERT INTO drink_flavors (drink_id, flavor_id) VALUES (%s, %s)",
                        (drink_id, flavor_id)
                    )
                    flavors_added.add(flavor_name)

        print(f"Inserted: {name}")

    conn.commit()

seed_drinks()