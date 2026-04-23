# tmdb.py
# This file handles all communication with the TMDB API.
# It contains functions that send requests and return clean, usable data.

import requests
from config import API_KEY

# The base URL for every TMDB API request
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """
    Searches for movies by title using the TMDB search endpoint.

    Parameters:
        title (str): The movie name the user typed in

    Returns:
        list: A list of movie dictionaries with results,
              or an empty list if nothing was found or an error occurred
    """

    # Build the full URL for the search endpoint
    # TMDB's search/movie endpoint lets us search by title (called "query")
    url = f"{BASE_URL}/search/movie"

    # Parameters we send along with the request:
    # - api_key: authenticates us with TMDB
    # - query: the search term (the movie title the user typed)
    # - language: ensures results come back in English
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US"
    }

    # Send the GET request to the TMDB API
    response = requests.get(url, params=params)

    # Check if the request was successful (status 200 = OK)
    if response.status_code == 200:
        # .json() converts the raw response text into a Python dictionary
        data = response.json()

        # The actual list of movies is inside the "results" key
        # Example: data = { "results": [ {movie1}, {movie2}, ... ] }
        return data["results"]

    else:
        # If something went wrong, print the error and return an empty list
        # This prevents the rest of the app from crashing
        print(f"❌ Error searching for movies. Status code: {response.status_code}")
        return []


def get_movie_details(movie_id):
    """
    Fetches full details about a specific movie using its TMDB ID.

    Parameters:
        movie_id (int): The unique TMDB ID for the movie

    Returns:
        dict: A dictionary with full movie details, or None if it failed
    """

    # The /movie/{movie_id} endpoint returns everything about a single movie
    url = f"{BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Return the full dictionary of movie details
        return response.json()
    else:
        print(f"❌ Error fetching movie details. Status code: {response.status_code}")
        return None