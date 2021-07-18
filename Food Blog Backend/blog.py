import argparse
from collections import defaultdict
import sqlite3


def execute_query(conn: sqlite3.Connection, sql_query: dict):
    cursor = conn.cursor()
    for query in sql_query:
        print(query)
        cursor.execute(sql_query[query])
    conn.commit()


def check_table(conn: sqlite3.Connection, table: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
    except sqlite3.OperationalError:
        return False
    return True


def select_query(conn: sqlite3.Connection, sql_query: str, values=None) -> list:
    if values is None:
        values = []
    cursor = conn.cursor()
    return cursor.execute(sql_query, values).fetchall()


def q_marks(values: list) -> str:
    return ",".join("?" for _ in range(len(values)))


def create_database(conn: sqlite3.Connection):
    schema = {
        "meals": """
            CREATE TABLE IF NOT EXISTS meals (
                meal_id INTEGER PRIMARY KEY,
                meal_name TEXT NOT NULL UNIQUE
            )
        """,
        "measures": """
            CREATE TABLE IF NOT EXISTS measures (
                measure_id INTEGER PRIMARY KEY,
                measure_name TEXT UNIQUE
            );
        """,
        "ingredients": """
            CREATE TABLE IF NOT EXISTS ingredients (
                ingredient_id INTEGER PRIMARY KEY,
                ingredient_name TEXT NOT NULL UNIQUE
            )
        """,
        "recipes": """
            CREATE TABLE IF NOT EXISTS recipes (
                recipe_id INTEGER PRIMARY KEY,
                recipe_name TEXT NOT NULL,
                recipe_description TEXT
            );
        """,
        "serve": """
            CREATE TABLE IF NOT EXISTS serve (
                serve_id INTEGER PRIMARY KEY,
                recipe_id INTEGER NOT NULL,
                meal_id INTEGER NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id)
            )
        """,
        "quantity": """
            CREATE TABLE IF NOT EXISTS quantity (
                quantity_id INTEGER PRIMARY KEY,
                measure_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                FOREIGN KEY (measure_id) REFERENCES measures (measure_id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id),
                FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id)
            )
        """,
    }
    data = {
        "meals": """
            INSERT INTO meals (meal_name) 
            VALUES ("breakfast"), ("brunch"), ("lunch"), ("supper")
        """,
        "measures": """
            INSERT INTO measures (measure_name)
            VALUES ("ml"), ("g"), ("l"), ("cup"), ("tbsp"), ("tsp"), ("dsp"), ("")
        """,
        "ingredients": """
            INSERT INTO ingredients (ingredient_name)
            VALUES ("milk"), ("cacao"), ("strawberry"),
            ("blueberry"), ("blackberry"), ("sugar")
        """,
    }

    print("Creating schema...")
    execute_query(conn, schema)
    print("Loading initial data...")
    execute_query(conn, data)


def fill_recipes(conn: sqlite3.Connection):
    cursor = conn.cursor()
    print("\nPass the empty recipe name to exit.")
    while True:
        recipe_name = input("Recipe name: ")
        if not recipe_name:
            break
        recipe_description = input("Recipe description: ")
        recipe_id = cursor.execute(
            "INSERT INTO recipes (recipe_name, recipe_description) VALUES (?, ?)",
            (recipe_name, recipe_description),
        ).lastrowid
        conn.commit()

        print("1) breakfast  2) brunch  3) lunch  4) supper")
        serve = input("Enter proposed meals separated by a space: ").split()
        for meal in serve:
            cursor.execute(
                "INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?)",
                (meal, recipe_id),
            )
        conn.commit()

        while True:
            ingredient_line = input(
                "Input quantity of ingredient <press enter to stop>:"
            ).split()
            if not ingredient_line:
                break
            if len(ingredient_line) < 2 or len(ingredient_line) > 3:
                print("Use <quantity> [measure] <ingredient> format!")
                continue
            try:
                quantity = int(ingredient_line[0])
            except ValueError:
                print("Quantity should be integer!")
                continue
            measure_id = []
            if len(ingredient_line) == 3:
                measure = ingredient_line[1]
                measure_id = cursor.execute(
                    "SELECT * FROM measures WHERE measure_name LIKE ?",
                    [f"%{measure}%"],
                ).fetchall()
                if len(measure_id) != 1:
                    print("The measure is not conclusive!")
                    continue
            elif len(ingredient_line) == 2:
                measure_id = cursor.execute(
                    "SELECT * FROM measures WHERE measure_name = ''"
                ).fetchall()
            ingredient = ingredient_line[-1]
            ingredient_id = cursor.execute(
                "SELECT * FROM ingredients WHERE ingredient_name LIKE ?",
                [f"%{ingredient}%"],
            ).fetchall()
            if len(ingredient_id) != 1:
                print("The ingredient is not conclusive!")
                continue
            cursor.execute(
                "INSERT INTO quantity (quantity, measure_id, ingredient_id, recipe_id) VALUES (?, ?, ?, ?)",
                (quantity, measure_id[0][0], ingredient_id[0][0], recipe_id),
            )
            conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Food blog backend")
    parser.add_argument("db_name", help="Database file name", default="food_blog.db")
    parser.add_argument("--ingredients", help="Ingredients, as comma separated list")
    parser.add_argument("--meals", help="Meals, as comma separated list")
    args = parser.parse_args()
    db_name = args.db_name
    ingredients = args.ingredients
    meals = args.meals

    connection = sqlite3.connect(db_name)
    if not check_table(connection, "meals"):
        create_database(connection)

    if not (ingredients or meals):
        fill_recipes(connection)
    else:
        recipe_ids_i = set()
        recipe_ids_m = set()
        if ingredients:
            ingredients_map = defaultdict(set)
            for row in select_query(
                connection,
                """
                    SELECT recipe_id, ingredient_name
                    FROM quantity q, ingredients i
                    WHERE q.ingredient_id = i.ingredient_id
                """,
            ):
                ingredients_map[row[0]].add(row[1])
            ingredients = set(ingredients.split(","))
            recipe_ids_i = set(
                recipe
                for recipe in ingredients_map
                if ingredients.issubset(ingredients_map[recipe])
            )
        if meals:
            meals = meals.split(",")
            recipe_ids_m = set(
                row[0]
                for row in select_query(
                    connection,
                    f"""
                    SELECT recipe_id
                    FROM serve s, meals m
                    WHERE m.meal_id = s.meal_id AND meal_name IN ({q_marks(meals)})
                """,
                    meals,
                )
            )
        recipe_ids = list(recipe_ids_i.intersection(recipe_ids_m))
        recipes = [
            row[0]
            for row in select_query(
                connection,
                f"SELECT recipe_name FROM recipes WHERE recipe_id IN ({q_marks(recipe_ids)});",
                recipe_ids,
            )
        ]
        if recipes:
            print(f"Recipes selected for you: {', '.join(recipes)}")
        else:
            print("There are no such recipes in the database.")
    connection.close()
