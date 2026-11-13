# tmdb.py
#
# Handles all communication with the TMDB (The Movie Database) API.
#
# Every request to TMDB goes through this file. The rest of the app
# (app.py, main.py) never builds TMDB URLs or handles API keys directly:
# it just calls these functions and gets back plain Python data.
#
# The API key comes from config.py, which is listed in .gitignore
# so it is never pushed to GitHub.

import requests
from config import API_KEY

# Every TMDB endpoint starts with this address
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """
    Searches TMDB for movies matching a title.

    Used by the /search route in app.py (modal search) and by main.py.

    Parameters:
        title (str): The text the user typed, e.g. "amadeus"

    Returns:
        list: Movie dictionaries in TMDB's raw format, best matches first.
              Each one has keys like "id", "title", "release_date",
              "vote_average" and "poster_path".
              Returns an empty list if the request fails, so callers
              can always loop over the result without checking for errors.
    """

    url = f"{BASE_URL}/search/movie"

    # requests turns this dictionary into the query string:
    # ?api_key=...&query=amadeus&language=en-US
    # It also escapes spaces and accents in the title for us.
    params = {
        "api_key": API_KEY,
        "query": title,
        "language": "en-US"
    }

    response = requests.get(url, params=params)

    # 200 means success. Anything else (401 = bad API key,
    # 429 = too many requests, 5xx = TMDB is down) is treated as a failure.
    if response.status_code == 200:
        data = response.json()

        # TMDB wraps the movies with pagination info:
        # { "page": 1, "results": [...], "total_pages": ..., "total_results": ... }
        # We only need the list itself.
        return data["results"]

    else:
        print(f"Error searching for movies. Status code: {response.status_code}")
        return []


def get_movie_details(movie_id):
    """
    Fetches the full details of one movie by its TMDB ID.

    Returns more than search_movie() does: genres, runtime, overview, etc.
    Not used anywhere in the app yet.

    Parameters:
        movie_id (int): The TMDB ID of the movie, e.g. 279 for Amadeus

    Returns:
        dict: All the movie's details, or None if the request failed.
    """

    # The ID goes in the URL path, not in the params: /movie/279
    url = f"{BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching movie details. Status code: {response.status_code}")
        return None