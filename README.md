**Prep and Go: Meal Prep Service**
A command-line interface (CLI) meal-planning tool that:
Fetches recipes and ingredient data from the Spoonacular Food API.
Generates concise summaries of each recipe or meal idea using Google Gemini AI.
Stores requests, generated meal plans (scaled by number of people), and user feedback in a SQLite database.

**The Features**
Budget-aware planning: Specify a maximum spend per meal (in USD).
Servings: Enter how many people you’re cooking for (scales ingredients and cost accordingly).
Dietary restrictions: Filter recipes by common diets (vegetarian, vegan, gluten free, dairy free).
AI summaries: Use Gemini to summarize recipe details.
Persistent storage: All inputs, results, and feedback saved in mealplanner.db.
User feedback: Prompt for satisfaction and comments to improve future suggestions.

**Some Prerequisites**
Python 3.7 or higher.
Spoonacular API key (Sign up here: https://spoonacular.com/food-api/console#Dashboard).
A Google Cloud service-account JSON key with access to Gemini.

**How to Install**
Clone the repository:
git clone https://github.com/yourusername/meal-planner-cli.git
cd meal-planner-cli
Set environment variables:
export SPOON_API_KEY="your_spoonacular_api_key"
export GOOGLE_API_KEY="/path/to/your/google-service-account.json"

**How to Use**
Run the main program: python3 mealPrep.py.
Enter your maximum spend per meal (e.g., 10.50).
Enter how many people/servings you’re cooking for (e.g., 4).
Provide comma-separated dietary restrictions (optional).
View a list of 3 suggested recipes with costs (scaled by servings) and AI summaries.
Get a consoladated shopping list upon request based on the recipes generated.
Answer whether you’re satisfied (yes/no) and optionally leave comments.
All data is recorded in mealplanner.db.



