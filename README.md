Python Recipe Finder and Meal Planner

This is a simple command-line application written in Python that allows you to search for recipes, add them to a weekly meal plan, and save your plan to a file. It uses the Spoonacular API to fetch recipe data.

🚀 Features

    Recipe Search: Find recipes by keyword or ingredient using the Spoonacular API.

    Weekly Meal Plan: Add selected recipes to a weekly meal schedule.

    Save & Load: Save your complete meal plan to a meal_plan.json file for future use.

📋 Prerequisites

Before you can run this application, you need to get a free API key from Spoonacular.

    Go to the Spoonacular website.

    Sign up for a free account.

    Navigate to your account dashboard and find your API key.

🛠️ Setup

    Clone the repository:
    Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Install the required libraries:
This project uses the requests library to make API calls. You can install it using pip:
Bash

pip install requests

Add your API Key:
Open the code_01.py file and replace the placeholder value for API_KEY with your actual key from Spoonacular.
Python

    # Add your api key here
    API_KEY = "YOUR_API_KEY_HERE"

💻 How to Use

To run the application, simply execute the Python script from your terminal:
Bash

python code_01.py

You will be presented with a main menu to guide you through the application's functions:

    Find Recipes by Ingredient: Enter a search term (e.g., "pasta" or "chicken"). The program will display a list of matching recipes.

    View Weekly Meal Plan: See your current meal plan for each day of the week.

    Add a Recipe to the Meal Plan: Choose a recipe from your search results and assign it to a specific day and meal time (e.g., Monday, Lunch).

    Save Meal Plan to File: Save your entire weekly plan to a file named meal_plan.json.

    Exit: Close the program.

📄 Code Structure

The code is organized into a few key functions:

    get_recipes_from_api(query, api_key): Fetches a list of basic recipe information (title, ID).

    get_recipe_details(recipe_id, api_key): Makes a second API call to get the full recipe details (ingredients and instructions) using the recipe ID.

    add_to_meal_plan(day, meal_type, recipe, plan): Adds a complete recipe dictionary to your weekly plan.

    save_meal_to_plan(plan, filename): Writes the meal plan data to a JSON file.
    took help from ai to writereadme.md file sorry guys 
    

    display_menu(): Prints the interactive menu for the user.

    main(): The primary function that runs the application loop.
