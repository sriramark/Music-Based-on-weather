import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "http://api.openweathermap.org"

def get_weather_data(city: str) -> dict | None:
    """Fetches current weather for a city."""
    if not OWM_API_KEY:
        print("ERROR: OpenWeatherMap API key not found in .env file.")
        return None

    try:
        # Geocoding to get coordinates
        geo_url = f"{BASE_URL}/geo/1.0/direct?q={city}&limit=1&appid={OWM_API_KEY}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return None

        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

        # Current weather
        current_url = f"{BASE_URL}/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={OWM_API_KEY}"
        current_response = requests.get(current_url)
        current_response.raise_for_status()
        current_data = current_response.json()

        return {
            "city": city,
            "description": current_data['weather'][0]['description'],
            "main_condition": current_data['weather'][0]['main'],
            "temp": current_data['main']['temp'],
            "feels_like": current_data['main']['feels_like'],
            "humidity": current_data['main']['humidity'],
            "wind_speed": current_data['wind']['speed'],
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error processing weather data structure: {e}")
        return None

