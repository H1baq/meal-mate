from db.models import Recipe, RecipeIngredient, Inventory, MealPlan
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("sqlite:///db/meal_mate.db")
Session = sessionmaker(bind=engine)

def list_recipes():
    session = Session()
    recipes = session.query(Recipe).all()
    session.close()
    return [{"id": r.id, "name": r.name} for r in recipes]

def check_inventory(recipe_dict):
    session = Session()
    recipe_id = recipe_dict['id']
    required_ingredients = session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).all()
    
    missing = []
    for req in required_ingredients:
        inventory = session.query(Inventory).filter_by(ingredient_id=req.ingredient_id).first()
        have = inventory.quantity_in_stock if inventory else 0
        if have < req.quantity_needed:  # ✅ FIXED HERE
            missing.append({
                "name": req.ingredient.name,
                "needed": req.quantity_needed,  # ✅ FIXED HERE
                "have": have
            })
    session.close()
    return missing

def create_meal_plan(date_str, recipe_dict):
    """Save a meal plan with the given date and recipe ID."""
    session = Session()
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        new_plan = MealPlan(date=date_obj, recipe_id=recipe_dict['id'])
        session.add(new_plan)
        session.commit()
        print(f"Meal plan for {date_str} added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to create meal plan: {e}")
    finally:
        session.close()
