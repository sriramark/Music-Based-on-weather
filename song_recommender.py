import os
import requests
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# A fallback song in case the API fails or returns no results
FALLBACK_SONG = {"title": "Bohemian Rhapsody", "artist": "Queen"}

def fetch_song_recommendation(mood: str) -> dict:
    """
    Fetches a popular song from Last.fm based on a mood tag.
    
    Args:
        mood: The mood to use as a query tag (e.g., "happy", "sad").

    Returns:
        A dictionary containing the song title and artist.
    """
    if not LASTFM_API_KEY:
        print("ERROR: Last.fm API key not found in .env file. Returning fallback song.")
        return FALLBACK_SONG

    params = {
        'method': 'tag.gettoptracks',
        'tag': mood,
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'limit': 50  # A pool of 50 songs to choose from
    }

    try:
        response = requests.get(LASTFM_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        tracks = data.get('tracks', {}).get('track', [])

        if not tracks:
            print(f"Warning: No tracks found for mood tag '{mood}'. Returning fallback song.")
            return FALLBACK_SONG

        # A random track from the top results
        random_track = random.choice(tracks)
        
        return {
            "title": random_track['name'],
            "artist": random_track['artist']['name']
        }

    except requests.exceptions.RequestException as e:
        print(f"Error calling Last.fm API: {e}. Returning fallback song.")
        return FALLBACK_SONG
    except (KeyError, IndexError) as e:
        print(f"Error parsing Last.fm response: {e}. Returning fallback song.")
        return FALLBACK_SONG

