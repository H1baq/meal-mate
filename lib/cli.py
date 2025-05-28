from helpers import get_user_input, validate_positive_number, format_table
from db_operations import load_inventory, save_ingredient, create_meal_plan, list_recipes, check_inventory, save_recipe_with_ingredients

def main():
    print("Welcome to Meal Mate!")
    while True:
        print("\nChoose an option:")
        print("1. Add Ingredient")
        print("2. Plan a Meal")
        print("3. View Inventory")
        print("4. Add Recipe")
        print("5. Exit")
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
    meal_date = get_user_input("Enter meal date (YYYY-MM-DD): ")
    recipes = list_recipes()

    if not recipes:
        print("No recipes available.")
        return

    print("\nAvailable recipes:")
    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe['name']}")

    choice = get_user_input("Select recipe number: ")

    if not choice.isdigit() or not (1 <= int(choice) <= len(recipes)):
        print("Invalid recipe choice.")
        return

    selected_recipe = recipes[int(choice) - 1]
    missing = check_inventory(selected_recipe)

    if missing:
        print("You are missing the following ingredients for this recipe:")
        for ing in missing:
            print(f"- {ing['name']} (need {ing['needed']}, have {ing['have']})")
    else:
        print("You have all ingredients needed for this recipe.")

    create_meal_plan(meal_date, selected_recipe)
    print(f"Meal plan for {meal_date} with recipe '{selected_recipe['name']}' saved.")

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

if __name__ == "__main__":
    main()
