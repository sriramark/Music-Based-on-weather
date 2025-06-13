Mood & Music AI API
Version: 1.0.0
Author: Sriram Krishnakumar
Tech Stack: FastAPI, Python, Pytest, OpenWeatherMap API, Google Gemini API, Last.fm API

# 1. Project Description:
   This application serves as an intelligent song recommendation engine. It takes a user's current mood and city as input, analyzes the real-time weather for that location using external APIs, and determines if the weather contextually aligns with the user's mood.

   The core of this project is its AI-driven logic. Instead of a rigid, hard-coded rules, this application delegates the complex task of weather-mood analysis to the Google Gemini API. Song recommendations are fetched dynamically from the Last.fm API based on mood tags.

# 2. Architecture
   The application is built using a modular architecture to ensure separation of concerns.

   main.py: The FastAPI server entry point.

   weather.py: A service module responsible for all communication with the OpenWeatherMap API.

   gemini_client.py: A service module that handles all communication with the Google Gemini API for mood analysis.

   song_recommender.py: A service module to handle all interactions with the Last.fm API for fetching songs.

   .env: A configuration file to securely store all API keys, keeping them separate from the source code.

   test_main.py: A dedicated module for unit testing.

# 3.  Design Philosophy & Future Work
   The AI-First Approach
   A key requirement of this project was to implement the "mood-weather matching" logic. Initial research (see reference folder) showed that the relationship between weather and human mood is quite complex, subjective, and dependent on both recent weather patterns and long-term climate context.

   Given this complexity, a decision was made to delegate the core reasoning to an AI model (Google Gemini) rather than building a rigid, hard-coded rules engine. This approach has several advantages:

   Nuance and Context: The AI can understand subtle ideas like "rain in a typically dry region is a happy event," which is not ideal to hard-code.

   Maintainability: The logic can be updated by refining the AI prompt rather than rewriting complex code.

   Scalability: It demonstrates a modern, scalable approach to solving complex, non-deterministic problems.

    Future Work: A Self-Improving Model
    While using a general-purpose AI like Gemini is powerful, a more cost-effective and specialized solution would be to train a custom machine learning model. The primary obstacle to this approach was the lack of large, publicly available datasets directly linking weather data to user moods.

    This application is designed to solve that problem. The main.py module can have a logging feature that records the user's mood and the AI's prediction for every request. Over time, this will build a valuable, proprietary dataset.

    A future version of this project could use this logged data to train a custom classification model. This "learning model" would become more accurate and tailored to the application's specific use case over time, potentially reducing the reliance on the more expensive general-purpose AI for the core logic.

# 4.  Setup and Installation
    Follow these steps to run the application locally.

    Prerequisites:

        1. Python 3.8+
        2. An active OpenWeatherMap API Key.
        3. An active Google Gemini API Key.
        4. An active Last.fm API Key.

    Step 1: Create the Environment File
    Create a file named .env in the root of your project folder and add your API keys:

    .env

    OWM_API_KEY="your_actual_openweathermap_api_key"
    GEMINI_API_KEY="your_actual_gemini_api_key"
    LASTFM_API_KEY="your_actual_lastfm_api_key"

    Step 2: Install Dependencies
    It is recommended to use a virtual environment.

    Create a virtual environment

    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`

    Install requirements

    pip install -r requirements.txt

    Step 3: Run the FastAPI Server
    Use uvicorn to start the local server.
    uvicorn main:app --reload

    The server will be running at http://127.0.0.1:8000. You can access the interactive API documentation at http://127.0.0.1:8000/docs.

# 5.  Unit Testing
    This project uses pytest for unit testing. The tests are designed to run without making real API calls by "mocking" the external services. This ensures that we are only testing the application's internal logic.

    To run the tests:

    Simply run the following command in your terminal from the project's root directory:

    pytest

# 6.  References & Further Reading
    The decision to use an AI-driven approach was informed by research into the complex nature of the weather-mood relationship. The following resources provide context on the scientific findings that make a simple hard-coded rules engine insufficient.

    Healthline: Yes, Weather Can Affect Your Mood and Energy — and So Can Climate Change - A good overview of how sunlight, temperature, and humidity impact mood.

    PLOS One Scientific Journal: Weather impacts expressed sentiment - A large-scale study analyzing billions of social media posts to show a correlation between meteorological conditions and expressed sentiment.

    Frontiers in Psychology: Season and Weather Effects on Travel-Related Mood - A study highlighting that different weather conditions (temperature, sunshine, wind) affect mood differently depending on context (e.g., travel mode).
