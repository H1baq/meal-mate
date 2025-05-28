from db.models import Ingredient, Inventory, MealPlan, Recipe, RecipeIngredient
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("sqlite:///db/meal_mate.db")
Session = sessionmaker(bind=engine)


def list_recipes():
    with Session() as session:
        recipes = session.query(Recipe).all()
        return [{"id": r.id, "name": r.name} for r in recipes]


def check_inventory(recipe_dict):
    """
    Check inventory in a single query with joins to avoid N+1 problem.
    """
    with Session() as session:
        recipe_id = recipe_dict['id']
        # Query RecipeIngredients with Ingredients and Inventories joined
        reqs = (
            session.query(RecipeIngredient)
            .join(RecipeIngredient.ingredient)
            .outerjoin(Inventory, Inventory.ingredient_id == RecipeIngredient.ingredient_id)
            .filter(RecipeIngredient.recipe_id == recipe_id)
            .all()
        )

        missing = []
        for req in reqs:
            have = req.ingredient.inventory.quantity_in_stock if req.ingredient.inventory else 0
            if have < req.quantity_needed:
                missing.append({
                    "name": req.ingredient.name,
                    "needed": req.quantity_needed,
                    "have": have,
                    "unit": req.unit,
                })
        return missing


def save_ingredient(name, quantity, unit):
    """
    Save or update ingredient and inventory atomically.
    """
    if unit not in {"grams", "ml", "pcs"}:
        raise ValueError(f"Invalid unit '{unit}'")

    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    with Session() as session:
        try:
            ingredient = session.query(Ingredient).filter_by(name=name).first()
            if not ingredient:
                ingredient = Ingredient(name=name, unit=unit)
                session.add(ingredient)
                session.flush()  # To get id without commit

            inventory = session.query(Inventory).filter_by(ingredient_id=ingredient.id).first()
            if inventory:
                inventory.quantity_in_stock += quantity
            else:
                inventory = Inventory(ingredient_id=ingredient.id, quantity_in_stock=quantity, unit=unit)
                session.add(inventory)

            session.commit()
        except Exception:
            session.rollback()
            raise


def save_recipe_with_ingredients(recipe_name, ingredients):
    """
    Save a recipe and all its ingredients atomically.
    """
    with Session() as session:
        try:
            existing = session.query(Recipe).filter_by(name=recipe_name).first()
            if existing:
                print(f"Recipe '{recipe_name}' already exists.")
                return False

            recipe = Recipe(name=recipe_name)
            session.add(recipe)
            session.flush()  # To get recipe.id

            for ing in ingredients:
                if ing['unit'] not in {"grams", "ml", "pcs"}:
                    raise ValueError(f"Invalid unit '{ing['unit']}' for ingredient {ing['name']}")
                if ing['quantity'] <= 0:
                    raise ValueError(f"Quantity must be positive for ingredient {ing['name']}")

                ingredient = session.query(Ingredient).filter_by(name=ing['name']).first()
                if not ingredient:
                    ingredient = Ingredient(name=ing['name'], unit=ing['unit'])
                    session.add(ingredient)
                    session.flush()

                recipe_ing = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity_needed=ing['quantity'],
                    unit=ing['unit']
                )
                session.add(recipe_ing)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error saving recipe: {e}")
            return False
        
def load_inventory():
    with Session() as session:
        inventories = (
            session.query(Inventory)
            .join(Ingredient)
            .all()
        )
        return [
            {
                "Ingredient": inv.ingredient.name,
                "Quantity": inv.quantity_in_stock,
                "Unit": inv.unit
            } for inv in inventories
        ]



def create_meal_plan(date_str, recipe_dict):
    """
    Save meal plan; handle unique constraint error gracefully.
    """
    with Session() as session:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Check for existing meal plan for date & recipe
            existing_plan = session.query(MealPlan).filter_by(date=date_obj, recipe_id=recipe_dict['id']).first()
            if existing_plan:
                print(f"Meal plan for {date_str} already exists with ID {existing_plan.id}.")
                return False

            new_plan = MealPlan(date=date_obj, recipe_id=recipe_dict['id'])
            session.add(new_plan)
            session.commit()
            print(f"Meal plan for {date_str} added successfully with ID {new_plan.id}.")
            return True
        except Exception as e:
            session.rollback()
            print(f"Failed to create meal plan: {e}")
            return False
