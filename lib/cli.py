from helpers import get_user_input, validate_positive_number, format_table, parse_date,confirm_action
from db_operations import list_recipes, check_inventory, create_meal_plan, save_ingredient, save_recipe_with_ingredients, load_inventory
from db_operations import (
    list_recipes,
    check_inventory,
    save_ingredient,
    create_meal_plan,
    save_recipe_with_ingredients,
    update_ingredient_quantity,
    delete_ingredient,
    delete_recipe
)



def main():
    print("Welcome to Meal Mate!")
    while True:
        print("\nChoose an option:")
        print("1. Add Ingredient")
        print("2. Plan a Meal")
        print("3. View Inventory")
        print("4. Add Recipe")
        print("5. Update Ingredient Quantity")
        print("6. Delete Ingredient")
        print("7. Delete Recipe")
        print("8. Exit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            add_ingredient()
        elif choice == '2':
            plan_meal()
        elif choice == '3':
            view_inventory()
        elif choice == '4':
            add_recipe()
        elif choice == '5':
            update_ingredient_quantity_cli()
        elif choice == '6':
            delete_ingredient_cli()  
        elif choice == '7':
            delete_recipe_cli()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


def add_ingredient():
    name = get_user_input("Enter ingredient name: ")
    quantity_input = get_user_input("Enter quantity: ")
    qty = validate_positive_number(quantity_input)

    while qty is None:
        print("Please enter a valid positive number.")
        quantity_input = get_user_input("Enter quantity: ")
        qty = validate_positive_number(quantity_input)

    unit = get_user_input("Enter unit (e.g., grams, ml, pcs): ")
    save_ingredient(name, qty, unit)
    print(f"Ingredient '{name}' with quantity {qty} {unit} added to inventory.")

def plan_meal():
    while True:
        meal_date_str = get_user_input("Enter meal date (YYYY-MM-DD): ")
        meal_date = parse_date(meal_date_str)
        if meal_date is None:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")
        else:
            break

    recipes = list_recipes()

    if not recipes:
        print("No recipes available.")
        return

    print("\nAvailable recipes:")
    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe['name']}")

    print("Select recipe numbers separated by commas (e.g. 1,3,5):")
    choices = get_user_input("Your choices: ")

    try:
        selected_indexes = [int(x.strip()) - 1 for x in choices.split(",")]
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return

    selected_recipes = []
    for i in selected_indexes:
        if 0 <= i < len(recipes):
            selected_recipes.append(recipes[i])
        else:
            print(f"Recipe number {i+1} is invalid.")
            return

    # Aggregate missing ingredients across all recipes
    all_missing = []
    for recipe in selected_recipes:
        missing = check_inventory(recipe)
        if missing:
            all_missing.extend(missing)

    if all_missing:
        print("You are missing the following ingredients:")
        for ing in all_missing:
            print(f"- {ing['name']} (need {ing['needed']}, have {ing['have']})")
    else:
        print("You have all ingredients needed for the selected recipes.")

    for recipe in selected_recipes:
        create_meal_plan(meal_date_str, recipe)

    print(f"Meal plan for {meal_date_str} with {len(selected_recipes)} recipes saved.")


def view_inventory():
    inventory = load_inventory()

    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory:")
    print(format_table(inventory, headers=["Ingredient", "Quantity", "Unit"]))

def add_recipe():
    name = get_user_input("Enter recipe name: ")
    ingredients = []

    while True:
        ing_name = get_user_input("Enter ingredient name (or press Enter to finish): ", required=False)
        if not ing_name:
            break

        quantity_input = get_user_input("Enter quantity for this ingredient: ")
        qty = validate_positive_number(quantity_input)

        while qty is None:
            print("Please enter a valid positive number.")
            quantity_input = get_user_input("Enter quantity: ")
            qty = validate_positive_number(quantity_input)

        unit = get_user_input("Enter unit (e.g., grams, ml, pcs): ")
        ingredients.append({"name": ing_name, "quantity": qty, "unit": unit})

    success = save_recipe_with_ingredients(name, ingredients)
    if success:
        print(f"Recipe '{name}' added with {len(ingredients)} ingredients.")
    else:
        print("Failed to add recipe.")
        
def update_ingredient_quantity_cli():
    name = get_user_input("Enter ingredient name to update: ")
    quantity_input = get_user_input("Enter new quantity: ")
    qty = validate_positive_number(quantity_input)

    while qty is None:
        print("Please enter a valid positive number.")
        quantity_input = get_user_input("Enter new quantity: ")
        qty = validate_positive_number(quantity_input)

    success = update_ingredient_quantity(name, qty)
    if success:
        print(f"Ingredient '{name}' quantity updated to {qty}.")


def delete_ingredient_cli():
    name = get_user_input("Enter ingredient name to delete: ")
    if confirm_action(f"Are you sure you want to delete ingredient '{name}'? This action cannot be undone (y/n): "):
        success = delete_ingredient(name)
        if success:
            print(f"Ingredient '{name}' deleted.")
    else:
        print("Deletion cancelled.")


def delete_recipe_cli():
    name = get_user_input("Enter recipe name to delete: ")
    if confirm_action(f"Are you sure you want to delete recipe '{name}'? This action cannot be undone (y/n): "):
        success = delete_recipe(name)
        if success:
            print(f"Recipe '{name}' deleted.")
    else:
        print("Deletion cancelled.")
if __name__ == "__main__":
    main()
