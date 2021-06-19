import sqlite3
import sys


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
        "serve": """
            CREATE TABLE IF NOT EXISTS serve (
                serve_id INTEGER PRIMARY KEY,
                recipe_id INTEGER NOT NULL,
                meal_id INTEGER NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id)
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
        serve = input("When the dish can be served: ").split()
        for meal in serve:
            cursor.execute("INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?);", (meal, recipe_id))
        conn.commit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    else:
        db_name = "food_blog.db"

    connection = sqlite3.connect(db_name)
    print(f"Connecting to the database {db_name}...")
    if not check_table(connection, "meals"):
        create_database(connection)
    fill_recipes(connection)

    connection.close()
    print("Bye!")
