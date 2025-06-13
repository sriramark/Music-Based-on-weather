import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def get_mood_analysis(weather_data: dict) -> dict | None:
    """
    Asks Gemini to predict mood, describe climate, and provide a reason,
    expecting a JSON response.
    Returns a dictionary with the analysis.
    """
    if not GEMINI_API_KEY:
        print("ERROR: Gemini API key not found in .env file.")
        return None

    # New prompt instructing the model to return a JSON object.
    prompt = f"""
    Analyze the following weather data.

    Your task:
    1.  Based on the city name, determine its general climate.
    2.  Analyze the current weather in the context of that climate.
    3.  Determine the single most likely public mood from this list: Happy, Energetic, Cozy, Gloomy, Calm, Irritable, Relieved, Sad, Melancholy, Romantic.
    4.  Provide a brief reason for your mood choice.

    Respond with a single, valid JSON object with three keys: "climate", "mood", and "reason". Do not include any other text or markdown formatting.

    Weather Data:
    - City: {weather_data['city']}
    - Current Condition: {weather_data['main_condition']} ({weather_data['description']})
    - Current Temperature: {weather_data['temp']:.1f}°C (feels like {weather_data['feels_like']:.1f}°C)
    - Current Humidity: {weather_data['humidity']}%
    """

    # payload to request JSON output
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()
        
        # The response is a JSON string within the 'text' field.
        json_text = result['candidates'][0]['content']['parts'][0]['text']
        
        analysis = json.loads(json_text)

        # All required keys are present
        if "mood" in analysis and "climate" in analysis and "reason" in analysis:
            return analysis
        else:
            print("Error: Gemini response missing required keys.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing Gemini response structure: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Gemini response: {e}")
        return None

