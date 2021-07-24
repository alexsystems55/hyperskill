from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meals(Base):
    __tablename__ = "meals"
    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.meal_name


class Measures(Base):
    __tablename__ = "measures"
    measure_id = Column(Integer, primary_key=True)
    measure_name = Column(String, unique=True)

    def __repr__(self):
        return self.measure_name


class Ingredients(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.ingredient_name


class Recipes(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String, nullable=False, unique=True)
    recipe_description = Column(String)

    def __repr__(self):
        return self.recipe_name


class Serve(Base):
    __tablename__ = "serve"
    serve_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.meal_id"), nullable=False)


class Quantity(Base):
    __tablename__ = "quantity"
    quantity_id = Column(Integer, primary_key=True)
    measure_id = Column(Integer, ForeignKey("measures.measure_id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), nullable=False)
