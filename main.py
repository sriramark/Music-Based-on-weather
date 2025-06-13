from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Set

from weather import get_weather_data
from gemini_client import get_mood_analysis
from song_recommender import fetch_song_recommendation


app = FastAPI(
    title="Mood & Music AI (Gemini Edition)",
    description="An API that uses the Gemini API to predict mood from weather and recommend a song.",
    version="1.0.0",
)

class UserInput(BaseModel):
    """Model for user input."""
    mood: str = Field(..., description="The user's current mood.", example="Happy")
    city: str = Field(..., description="The user's current city.", example="Ottapalam")

class Song(BaseModel):
    """Model for a song recommendation."""
    title: str
    artist: str

class AppResponse(BaseModel):
    """Model for the API response."""
    analysis: str
    predicted_mood: str
    reason_for_prediction: str
    song_recommendation: Song

MOOD_SIMILARITY: dict[str, Set[str]] = {
    "happy": {"energetic", "relieved", "calm"},
    "energetic": {"happy"},
    "cozy": {"calm", "happy"},
    "gloomy": {"sad", "melancholy"},
    "sad": {"gloomy", "melancholy"},
    "melancholy": {"gloomy", "sad"},
    "calm": {"cozy", "relieved"},
    "relieved": {"happy", "calm"},
    "angry": {"frustrated", "irritated"},
    "frustrated": {"angry", "irritated"},
    "tensed": {"frustrated", "irritable"},
    "irritable": {"angry", "frustrated", "boring"},
    "boring": {"disinterested", "uninspired", "irritable"},
}

@app.post("/recommend", response_model=AppResponse)
async def get_recommendation(user_input: UserInput) -> AppResponse:
    """
    Main endpoint to process user input and return a mood-based song recommendation.
    """
    # live weather data
    if not user_input.city or not user_input.mood:
        raise HTTPException(
            status_code=400,
            detail="Both 'city' and 'mood' fields are required."
        )

    weather_data = get_weather_data(user_input.city)
    if not weather_data:
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch weather data for {user_input.city}. Please check the city name or API keys. If the error persists, try again later."
        )

    # Get mood analysis from the Gemini API
    gemini_analysis = get_mood_analysis(weather_data)
    if not gemini_analysis:
        raise HTTPException(status_code=500, detail="Failed to get analysis from Gemini API.")

    user_mood = user_input.mood.lower()
    predicted_mood = gemini_analysis["mood"].lower()
    similar_moods = {m.lower() for m in MOOD_SIMILARITY.get(user_mood, set())}
    climate_info = gemini_analysis["climate"]
    mood_reason = gemini_analysis["reason"]

    # Compare user's mood with predicted mood for analysis text
    if user_mood == predicted_mood:
        analysis_text = (f"We get it! The weather in {user_input.city} ({climate_info}) totally matches your '{user_mood}' mood." )
    elif predicted_mood in similar_moods:
        analysis_text = (f"The weather in {user_input.city} feels very '{predicted_mood}', which is close to your '{user_mood}' mood.")
    else:
        analysis_text = (f"It seems the weather in {user_input.city} feels '{predicted_mood}', but you're feeling '{user_mood}'. Let's find a song for your mood!" )

    # Song recommendation
    song = fetch_song_recommendation(user_mood)

    return AppResponse(
        analysis=analysis_text,
        predicted_mood=predicted_mood,
        reason_for_prediction=mood_reason,
        song_recommendation=song
    )

