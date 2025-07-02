# Meal Prep Shopping List Automator (Google AI Studio version)
# Prompts user for meal budget & dietary restrictions
# Uses Gemini API to generate 5 meal prep ideas
# Saves to SQLite DB

import os
import sqlite3
import google.generativeai as genai
from database_functions import (
    init_db,
    save_request,
    save_meals,
    save_feedback
)

# Your AI Studio API Key
GOOGLE_API_KEY =''

if not GOOGLE_API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY environment variable not set.")
    print("Please set it like this in your terminal:")
    print('  export GOOGLE_API_KEY="YOUR_KEY_HERE"')
    exit(1)

# Initialize Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

DB_PATH = 'mealplanner.db'


def call_genai_for_meals(budget, diets):
    """Uses Gemini to generate 5 meal prep ideas as text."""
    diet_text = ', '.join(diets) if diets else "no dietary restrictions"
    prompt = (
        f"Suggest 5 meal prep recipes under ${budget} with {diet_text}.\n"
        f"For each recipe, provide:\n"
        f"- Title\n"
        f"- Estimated price (in USD)\n"
        f"- Diet tags (comma-separated)\n"
        f"- Source URL (can be a placeholder)\n"
    )

    response = model.generate_content(prompt)
    text = response.text

    # Parse: split on double newlines
    meals = []
    for block in text.strip().split("\n\n"):
        lines = block.strip().split("\n")
        meal = {"title": "", "price": 0.0, "diets": [], "summary": "", "source_url": ""}

        for line in lines:
            line = line.strip()
            if line.lower().startswith("title:"):
                meal["title"] = line.partition(":")[2].strip()
            elif line.lower().startswith("estimated price"):
                try:
                    price_text = line.partition(":")[2].strip().replace("$", "")
                    meal["price"] = float(price_text)
                except ValueError:
                    meal["price"] = 0.0
            elif line.lower().startswith("diet tags"):
                tags = line.partition(":")[2].strip()
                meal["diets"] = [tag.strip() for tag in tags.split(",") if tag.strip()]
            elif line.lower().startswith("source url"):
                meal["source_url"] = line.partition(":")[2].strip()

        if meal["title"]:
            meals.append(meal)

    return meals


if __name__ == "__main__":
    print("\n=== Welcome to the Meal Prep CLI (Gemini) ===")

    # 1. Init DB
    conn = init_db(DB_PATH)

    # 2. Get user budget
    while True:
        try:
            budget = float(input("Enter your meal budget (e.g. 25.0): ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    # 3. Get user dietary restrictions
    diets_input = input("Enter any dietary restrictions separated by commas (or leave blank): ").strip()
    diets = [d.strip() for d in diets_input.split(",") if d.strip()]

    # 4. Save request
    request_id = save_request(conn, budget, diets)
    print(f"\nRequest saved with ID {request_id}.")

    # 5. Call GenAI
    print("\nGenerating meal ideas with Gemini...")
    try:
        results = call_genai_for_meals(budget, diets)
    except Exception as e:
        print("\n⚠️ Error generating meal ideas.")
        print("Please check your API key and try again.")
        print(f"Details: {e}\n")
        conn.close()
        exit(1)

    if not results:
        print("\nNo meal ideas were generated. Please try with different parameters or later.")
        conn.close()
        exit(0)

    # 6. Show meals and prepare for DB insert
    meals_to_save = []
    print("\nHere are your meal suggestions:\n")

    for idx, meal in enumerate(results, start=1):
        print(f"Meal {idx}:")
        print(f"  Title: {meal['title']}")
        print(f"  Price Estimate: ${meal['price']:.2f}")
        print(f"  Diet Tags: {', '.join(meal['diets'])}")
        print(f"  Source URL: {meal['source_url']}")
        print()

        meals_to_save.append(meal)


# 7. Save meals to DB
save_meals(conn, request_id, meals_to_save)
print("\nMeals saved to database.")

    # 8. Collect feedback
print("\n--- Feedback ---")
feedback = input("Are you satisfied with these meal suggestions? (yes/no): ").strip().lower()
satisfied = feedback in ["yes", "y"]
comments = input("Any comments? (optional): ").strip()

save_feedback(conn, request_id, satisfied, comments)
print("Thank you! Your feedback has been saved.")

conn.close()
print("\n=== Meal Plan Session Complete ===\n")
...