import argparse
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_tables import Base, Ingredients, Meals, Measures, Recipes, Quantity, Serve


def init_database(session):
    print("Initializing database...")
    if len(session.query(Meals).all()) == 0:
        session.add_all(
            [
                Meals(meal_name="breakfast"),
                Meals(meal_name="brunch"),
                Meals(meal_name="lunch"),
                Meals(meal_name="supper"),
            ]
        )
    if len(session.query(Measures).all()) == 0:
        session.add_all(
            [
                Measures(measure_name="ml"),
                Measures(measure_name="g"),
                Measures(measure_name="l"),
                Measures(measure_name="cup"),
                Measures(measure_name="tbsp"),
                Measures(measure_name="tsp"),
                Measures(measure_name="dsp"),
                Measures(measure_name=""),
            ]
        )
    if len(session.query(Ingredients).all()) == 0:
        session.add_all(
            [
                Ingredients(ingredient_name="milk"),
                Ingredients(ingredient_name="cacao"),
                Ingredients(ingredient_name="strawberry"),
                Ingredients(ingredient_name="blueberry"),
                Ingredients(ingredient_name="blackberry"),
                Ingredients(ingredient_name="sugar"),
            ]
        )
    session.commit()


def fill_recipes(session):
    print("\nPass the empty recipe name to exit.")
    while True:
        recipe_name = input("Recipe name: ")
        if not recipe_name:
            break
        recipe_description = input("Recipe description: ")
        recipe = Recipes(recipe_name=recipe_name, recipe_description=recipe_description)
        session.add(recipe)
        session.commit()

        print("1) breakfast  2) brunch  3) lunch  4) supper")
        serve = input("Enter proposed meals separated by a space: ").split()
        for meal in serve:
            session.add(Serve(meal_id=meal, recipe_id=recipe.recipe_id))
        session.commit()

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
            measure = None
            if len(ingredient_line) == 3:
                measure_arg = ingredient_line[1]
                measure = (
                    session.query(Measures)
                    .filter_by(measure_name=measure_arg)
                    .one_or_none()
                )
                if not measure:
                    print("The measure is not conclusive!")
                    continue
            elif len(ingredient_line) == 2:
                measure = session.query(Measures).filter_by(measure_name="").first()
            ingredient_arg = ingredient_line[-1]
            ingredient = (
                session.query(Ingredients)
                .filter(Ingredients.ingredient_name.like(f"%{ingredient_arg}%"))
                .one_or_none()
            )
            if not ingredient:
                print("The ingredient is not conclusive!")
                continue
            session.add(
                Quantity(
                    quantity=quantity,
                    measure_id=measure.measure_id,
                    ingredient_id=ingredient.ingredient_id,
                    recipe_id=recipe.recipe_id,
                )
            )
            session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Food blog backend")
    parser.add_argument("db_name", help="Database file name", default="food_blog.db")
    parser.add_argument("--ingredients", help="Ingredients, as comma separated list")
    parser.add_argument("--meals", help="Meals, as comma separated list")
    args = parser.parse_args()
    db_name = args.db_name
    ingredients = args.ingredients
    meals = args.meals

    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    my_session = Session()
    init_database(my_session)

    if not (ingredients or meals):
        fill_recipes(my_session)
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
    my_session.close()
