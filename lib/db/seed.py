from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Base, Ingredient, Recipe, RecipeIngredient, Inventory, MealPlan

engine = create_engine("sqlite:///./meal_mate.db")
Session = sessionmaker(bind=engine)
session = Session()

def seed():
    # Clear existing data (optional)
    session.query(MealPlan).delete()
    session.query(Inventory).delete()
    session.query(RecipeIngredient).delete()
    session.query(Recipe).delete()
    session.query(Ingredient).delete()
    session.commit()

    # Ingredients
    flour = Ingredient(name="Flour", unit="grams")
    milk = Ingredient(name="Milk", unit="ml")
    eggs = Ingredient(name="Eggs", unit="pcs")
    sugar = Ingredient(name="Sugar", unit="grams")

    session.add_all([flour, milk, eggs, sugar])
    session.commit()

    # Recipe
    pancakes = Recipe(name="Pancakes",)
    session.add(pancakes)
    session.commit()

    # Link ingredients to recipe
    session.add_all([
        RecipeIngredient(recipe=pancakes, ingredient=flour, quantity_needed=200, unit="grams"),
        RecipeIngredient(recipe=pancakes, ingredient=milk, quantity_needed=300, unit="ml"),
        RecipeIngredient(recipe=pancakes, ingredient=eggs, quantity_needed=2, unit="pcs"),
        RecipeIngredient(recipe=pancakes, ingredient=sugar, quantity_needed=50, unit="grams"),
    ])
    session.commit()

    # Inventory stock
    session.add_all([
        Inventory(ingredient=flour, quantity_in_stock=500, unit="grams"),
        Inventory(ingredient=milk, quantity_in_stock=1000, unit="ml"),
        Inventory(ingredient=eggs, quantity_in_stock=6, unit="pcs"),
        Inventory(ingredient=sugar, quantity_in_stock=300, unit="grams"),
    ])
    session.commit()

    # Meal Plan
    session.add(MealPlan(date=date.today(), recipe=pancakes))
    session.commit()

    print("Seed data added successfully.")

if __name__ == "__main__":
    seed()
