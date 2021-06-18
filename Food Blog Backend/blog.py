import sqlite3
import sys


def execute_query(conn: sqlite3.Connection, sql_query: dict):
    cursor = conn.cursor()
    for query in sql_query:
        print(query)
        cursor.execute(sql_query[query])
    conn.commit()


def create_database(conn: sqlite3.Connection):
    schema = {
        "meals": """
            CREATE TABLE IF NOT EXISTS meals (
                meal_id INTEGER PRIMARY KEY,
                meal_name TEXT NOT NULL UNIQUE
            );
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
        );
        """,
        "recipes": """
            CREATE TABLE IF NOT EXISTS recipes (
                recipe_id INTEGER PRIMARY KEY,
                recipe_name TEXT NOT NULL,
                recipe_description TEXT
        );
        """,
    }
    data = {
        "meals": """
            INSERT INTO meals (meal_name) 
            VALUES ("breakfast"), ("brunch"), ("lunch"), ("supper");
        """,
        "measures": """
            INSERT INTO measures (measure_name)
            VALUES ("ml"), ("g"), ("l"), ("cup"), ("tbsp"), ("tsp"), ("dsp"), ("");
        """,
        "ingredients": """
            INSERT INTO ingredients (ingredient_name)
            VALUES ("milk"), ("cacao"), ("strawberry"),
            ("blueberry"), ("blackberry"), ("sugar");
        """,
    }

    print("Creating schema...")
    execute_query(conn, schema)
    print("Loading initial data...")
    execute_query(conn, data)


def fill_recipes(conn: sqlite3.Connection):
    cursor = conn.cursor()
    while True:
        recipe_name = input("Enter recipe name or empty string to exit: ")
        if not recipe_name:
            break
        recipe_description = input("Enter cooking directions: ")
        cursor.execute(
            "INSERT INTO recipes (recipe_name, recipe_description) VALUES (?, ?)",
            (recipe_name, recipe_description),
        )
    conn.commit()


if __name__ == "__main__":
    db_name = sys.argv[1]
    print(f"Connecting to the database {db_name}...")
    connection = sqlite3.connect(db_name)

    create_database(connection)
    fill_recipes(connection)

    connection.close()
