import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json

load_dotenv()

APP_ID = os.getenv("API_ID")
API_KEY = os.getenv("API_KEY")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT = "https://api.sheety.co/929885b185c91a829b0521e7a7090ea6/myWorkoutLog/workouts"

# Home Route
@ensure_csrf_cookie
@csrf_exempt
def log_workout(request):
    if request.method == 'POST':
        exercise_text = request.POST['exercise_text']
        gender = request.POST['gender']
        weight_kg = request.POST['weight_kg']
        height_cm = request.POST['height_cm']
        age = request.POST['age']
        headers = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
        }
        parameters = {
            "query": exercise_text,
            "gender": gender,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "age": age
        }
        try:
            response = requests.post(
                EXERCISE_ENDPOINT, json=parameters, headers=headers)
            result = response.json()
            today_date = datetime.now().strftime("%d/%m/%Y")
            now_time = datetime.now().strftime("%X")
            for exercise in result["exercises"]:
                sheet_inputs = {
                    "workout": {
                        "date": today_date,
                        "time": now_time,
                        "exercise": exercise["name"].title(),
                        "duration": exercise["duration_min"],
                        "calories": exercise["nf_calories"]
                    }
                }
                sheet_response = requests.post(
                    SHEET_ENDPOINT, json=sheet_inputs)
                print(sheet_response.text)
            return render(request, 'success.html')
        except requests.exceptions.RequestException:
            return render(request, 'error.html')
    return render(request, 'index.html')


# Route for the fetch API data
def fetch_api_data(request):
    # Make API request using requests library
    response = requests.get(url=SHEET_ENDPOINT)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render(request, 'api_data.html', {'data': data})
    else:
        error_message = "Unauthorized. A valid 'Authorization' header is required to access this API."
        return render(request, 'api_error.html', {'error_message': error_message})



