# Meal Mate

Meal Mate is a simple meal planning CLI program built with Python and SQLAlchemy, designed to help users manage recipes, ingredients, inventory, and meal plans efficiently. The program stores data in a SQLite database and supports adding recipes, tracking ingredient inventory, and creating meal plans for specific dates.

---

## Project Overview

### CLI Script

The main interface to Meal Mate is a command-line script. It allows users to:

- List available recipes.
- Check ingredient inventory against recipes to identify missing items.
- Add new ingredients and update inventory stock.
- Save recipes with their ingredients.
- Create meal plans by assigning recipes to dates.

The script interacts with the database via SQLAlchemy ORM and handles user inputs and validations gracefully.

---

### Key Functions

- **list_recipes()**  
  Retrieves all recipes from the database and returns them with their IDs and names.

- **check_inventory(recipe_dict)**  
  Checks if there are sufficient ingredients in stock for the selected recipe, returning missing ingredients if any.

- **save_ingredient(name, quantity, unit)**  
  Adds a new ingredient or updates existing inventory quantities atomically, ensuring units are valid.

- **save_recipe_with_ingredients(recipe_name, ingredients)**  
  Saves a recipe and its associated ingredients, with validation for quantities and units.

- **create_meal_plan(date_str, recipe_dict)**  
  Creates a meal plan entry for a given date and recipe, handling duplicates and database constraints.

- **load_inventory()**  
  Loads current inventory stock details for all ingredients.

---

### Database Models

- **Ingredient**  
  Represents ingredients with name and unit (e.g., grams, ml, pcs).

- **Recipe**  
  Represents a recipe with a unique name (description was removed in migrations).

- **RecipeIngredient**  
  Links recipes to ingredients with quantity needed and unit.

- **Inventory**  
  Tracks current stock quantity for each ingredient.

- **MealPlan**  
  Maps recipes to specific dates, with unique constraints to avoid duplicate entries.

The models use relationships and foreign keys to enforce referential integrity.

---

### Database Setup

- The project uses **SQLite** as the database backend.
- Database schema and migrations are managed with **Alembic**.
- Initial migrations create all tables including ingredients, recipes, inventory, meal plans, and recipe ingredients.
- A `seed.py` script populates initial data for testing, including ingredients, a sample recipe (Pancakes), inventory stock, and a meal plan entry.

---

### Dependencies

- Python 3.x  
- SQLAlchemy  
- Alembic  

You can install dependencies with:

```bash
pip install -r requirements.txt

Typical User Workflow
Set up the database by running Alembic migrations:

bash
Copy code
alembic upgrade head
Seed initial data (ingredients, recipes, inventory) by running the seed script:

bash
Copy code
python seed.py
Use the CLI script to:

View recipes and ingredients.

Check inventory against recipes.

Add new ingredients or update stock.

Create meal plans by selecting recipes and dates.

Additional Notes
Inventory checks use optimized SQL queries with joins to avoid performance issues.

Units are strictly validated (grams, ml, pcs) to maintain data consistency.

Alembic is used for managing database schema versions; always run migrations before running the app after schema changes.

Author: 
Hibaq Adan Kuresh

Contact:
for any inquries reach out via hibaqku7@gmail.com

License under 
MIT


