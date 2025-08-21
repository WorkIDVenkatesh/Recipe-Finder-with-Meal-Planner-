import requests
import json 
# And main thing this code is written specific for spoonacular.com
#  Add you api key 
API_KEY = "6c94d60fef2544acb2100ef8a6284625744733" 
API_URL_SEARCH = "https://api.spoonacular.com/recipes/complexSearch"
API_URL_DETAILS = "https://api.spoonacular.com/recipes/{id}/information"

def get_recipes_from_api(query, api_key):
    
    try:
        params = {
            "query": query,
            "apiKey": api_key
        }
        response = requests.get(API_URL_SEARCH, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        recipes = []
        for result in data.get("results", []):
            recipe = {
                "id": result.get("id"),
                "name": result.get("title", "No Title"),
            }
            recipes.append(recipe)
        
        return recipes
    except requests.exceptions.RequestException as e:
        print(f"**Error:** Could not connect to the API. Details: {e}")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"**Error:** Failed to parse the API response. Details: {e}")
        return []

def get_recipe_details(recipe_id, api_key):
    
    try:
        url = API_URL_DETAILS.format(id=recipe_id)
        params = {
            "apiKey": api_key
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Get ingredients from the detailed response
        ingredients_list = [item.get("original") for item in data.get("extendedIngredients", [])]
        
        # Get instructions
        instructions = data.get("instructions", "No instructions available.")
        
        return {
            "name": data.get("title", "No Title"),
            "ingredients": ingredients_list,
            "instructions": instructions,
            "category": "General"
        }
    except requests.exceptions.RequestException as e:
        print(f"**Error:** Could not connect to the API to get recipe details. Details: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"**Error:** Failed to parse the API response for details. Details: {e}")
        return None

def save_meal_to_plan(plan, filename="meal_plan.json"):
    
    with open(filename, 'w') as f:
        json.dump(plan, f, indent=4)
    print(f"**Success:** Your meal plan has been saved to '{filename}'.")
    
def add_to_meal_plan(day, meal_type, recipe, plan):
    # Adds recipe to the meal plan if the day and meal type are valid.
    
    if day in plan and meal_type in plan[day]:
        plan[day][meal_type] = recipe
        print(f"**Success:** Added {recipe['name']} to {day}'s {meal_type}.")
    else:
        print("**Error:** Invalid day or meal type.")

def display_menu():
    """Prints the main menu options."""
    print("\n--- Main Menu ---")
    print("1. Find Recipes by Ingredient")
    print("2. View Weekly Meal Plan")
    print("3. Add a Recipe to the Meal Plan")
    print("4. Save Meal Plan to File")
    print("5. Exit")

def main():
    
    weekly_plan = {day: {"Breakfast": None, "Lunch": None, "Dinner": None} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    found_recipes_from_api = []

    while True:
        display_menu()
        choice = input("Enter Your Choice (1-5): ")

        if choice == '1':
            query = input("Enter a keyword or ingredient to search for: ")
            print(f"Searching for recipes with '{query}'...")
            
            found_recipes_from_api = get_recipes_from_api(query, API_KEY)
            
            if found_recipes_from_api:
                print("\n--- Found Recipes ---")
                for i, recipe in enumerate(found_recipes_from_api):
                    print(f"{i+1}. {recipe['name']}")
            else:
                print("No recipes found with that search term.")
        
        elif choice == '2':
            print("\n--- Your Weekly Meal Plan ---")
            for day, meals in weekly_plan.items():
                print(f"\n**{day}:**")
                for meal_type, recipe in meals.items():
                    recipe_name = recipe['name'] if recipe else "Not Planned"
                    print(f"  - {meal_type}: {recipe_name}")

        elif choice == '3':
            if not found_recipes_from_api:
                print("Please find recipes first using option 1.")
                continue
            
            try:
                recipe_index = int(input("Enter the number of the recipe to add: ")) - 1
                if not (0 <= recipe_index < len(found_recipes_from_api)):
                    print("Invalid recipe number. Please try again.")
                    continue

                day_choice = input("Enter the day (e.g., Monday): ").capitalize()
                meal_choice = input("Enter the meal type (Breakfast, Lunch, Dinner): ").capitalize()
                
                selected_recipe_id = found_recipes_from_api[recipe_index]["id"]
                
                print("Fetching full recipe details...")
                recipe_to_add = get_recipe_details(selected_recipe_id, API_KEY)
                
                if recipe_to_add:
                    add_to_meal_plan(day_choice, meal_choice, recipe_to_add, weekly_plan)
                else:
                    print("**Error:** Failed to fetch recipe details.")

            except (ValueError, NameError):
                print("**Error:** Invalid input. Please enter a number.")
        
        elif choice == '4':
            save = input("Do you want to save? (yes/no): ").lower()
            if save == 'yes':
                save_meal_to_plan(weekly_plan)
            elif save == 'no':
                print("Meal plan not saved.")
            else:
                print("**Error:** Invalid save format. Please choose 'yes' or 'no'.")
        
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":

    main()
