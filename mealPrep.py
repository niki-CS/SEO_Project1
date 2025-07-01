# Meal Prep Shopping List Automator
# Computer will prompt user for meal that they desire to meal prep for breakfast, lunch, and dinner
# Shopping list will be generated based on meals specified
# AI will generate general list based on web results of meal names
import os
import sqlite3
import requests
from google.cloud import aiplatform
from database_functions import (
    init_db,
    save_request,
    save_meals,
    save_feedback
)
SPOON_API_KEY = os.getenv('')
GOOGLE_API_KEY = os.getenv('')

DB_PATH = 'mealplanner.db'
# Introduction, call apis
def call_spoonacular(budget, diets):
    #Query Spoonacular for recipes under budget and matching diets.
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': SPOON_API_KEY,
        'maxPrice': budget,
        'number': 5,
        'addRecipeInformation': True,
        'diet': ','.join(diets) if diets else None,
    }
    resp = requests.get(url, params={k: v for k, v in params.items() if v})
    resp.raise_for_status()
    return resp.json().get('results', [])


def summarize_with_genai(text):
    #Use Google GenAI to summarize a recipe description.
    client = aiplatform.gapic.PredictionServiceClient.from_service_account_file(
        GOOGLE_API_KEY
    )
    response = client.predict(
        endpoint="projects/PROJECT/locations/LOCATION/endpoints/ENDPOINT_ID", #have to repalce with values, not sure how to proceed exactly, will discuss
        instances=[{"text": text}],
    )
    return response.predictions[0].get('summary', '')


# End of program? Ask user if satisfied with results?
