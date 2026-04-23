# NextWatch - Movie Recommendation System
# This file is the main entry point of the application

import requests
from config import API_KEY

# Base URL for all TMDB API requests
# Every endpoint we use will start with this URL
BASE_URL = "https://api.themoviedb.org/3"


def connect_to_api():
    """
    Tests the connection to the TMDB API.
    We use the /configuration endpoint because it is lightweight
    and only requires a valid API key to return a success response.
    """

    # Build the full URL for the configuration endpoint
    url = f"{BASE_URL}/configuration"

    # Parameters sent along with the request
    # The API key identifies who is making the request
    params = {"api_key": API_KEY}

    # Make a GET request to the TMDB API
    # A GET request means we are asking for data, not sending any
    response = requests.get(url, params=params)

    # Status code 200 means the request was successful
    # Any other code means something went wrong
    if response.status_code == 200:
        print("✅ Connected to TMDB API successfully!")
    else:
        print(f"❌ Connection failed. Status code: {response.status_code}")


# This block only runs when we execute this file directly
# It will not run if this file is imported by another file later
if __name__ == "__main__":
    connect_to_api()