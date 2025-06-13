from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_recommendation_success():
    """
    Tests the main success path of the /recommend endpoint.
    Uses @patch to simulate successful responses from all external APIs.
    """

    with patch('main.get_weather_data') as mock_get_weather, \
         patch('main.get_mood_analysis') as mock_get_mood, \
         patch('main.fetch_song_recommendation') as mock_fetch_song:

        #  fake data our mocked functions will return for this test.
        mock_get_weather.return_value = {"city": "London", "main_condition": "Clouds", "temp": 15.0}
        mock_get_mood.return_value = {"mood": "Calm", "climate": "Temperate", "reason": "A calm day."}
        mock_fetch_song.return_value = {"title": "Weightless", "artist": "Marconi Union"}

        response = client.post("/recommend", json={"mood": "Calm", "city": "London"})

        assert response.status_code == 200
        data = response.json()
        assert data["predicted_mood"] == "calm" # Checking against the lowercased version from main.py
        assert data["song_recommendation"]["title"] == "Weightless"
        assert "totally matches your 'calm' mood" in data["analysis"]


def test_recommendation_weather_service_fails():
    """
    Tests the failure case where the weather service cannot find the city.
    The application should gracefully handle this and return a 500 error as coded in main.py.
    """
    with patch('main.get_weather_data') as mock_get_weather:
        # Simulate the weather service failing by having it return None.
        mock_get_weather.return_value = None

        response = client.post("/recommend", json={"mood": "Happy", "city": "InvalidCity"})

        assert response.status_code == 500
        assert "Could not fetch weather data" in response.json()["detail"]


def test_recommendation_gemini_service_fails():
    """
    Tests the failure case where the Gemini service fails after a successful weather call.
    The application should return a 500 Internal Server Error.
    """
    with patch('main.get_weather_data') as mock_get_weather, \
         patch('main.get_mood_analysis') as mock_get_mood:
        
        # Simulate a successful weather call...
        mock_get_weather.return_value = {"city": "London", "main_condition": "Clouds", "temp": 15.0}
        # ...but a failed Gemini call.
        mock_get_mood.return_value = None

        response = client.post("/recommend", json={"mood": "Happy", "city": "London"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Failed to get analysis from Gemini API."


def test_recommendation_bad_request_missing_city():
    """
    Tests the failure case where the client forgets to include the 'city'.
    The application should return a validation error.
    """
    # No mocks needed as the error happens before external calls.
    
    # API CALL with invalid JSON
    response = client.post("/recommend", json={"mood": "Happy"}) # Missing "city"

    # 422 Unprocessable Entity error, which is FastAPI's default for validation errors.
    assert response.status_code == 422
    assert "field required" in response.text.lower()

