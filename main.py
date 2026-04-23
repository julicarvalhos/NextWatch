# main.py
# This is the main entry point of the application.
# For now, it tests the search functionality from tmdb.py.

import requests
from config import API_KEY
from tmdb import search_movie  # Import the function we just created

BASE_URL = "https://api.themoviedb.org/3"


def connect_to_api():
    """
    Tests the connection to the TMDB API.
    """
    url = f"{BASE_URL}/configuration"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("✅ Connected to TMDB API successfully!")
    else:
        print(f"❌ Connection failed. Status code: {response.status_code}")


def display_search_results(movies):
    """
    Prints the search results in a readable format.

    Parameters:
        movies (list): The list of movie dictionaries returned by search_movie()
    """

    # If the list is empty, there's nothing to show
    if not movies:
        print("No movies found.")
        return

    print("\n🎬 Search Results:")
    print("-" * 40)

    # Loop through the results with enumerate() so we get a number next to each one
    # We only show the first 5 results ([:5]) to avoid flooding the terminal
    for i, movie in enumerate(movies[:5], start=1):

        # "title" is the movie name
        # .get() is safer than [] — it returns a default value if the key doesn't exist
        title = movie.get("title", "Unknown Title")

        # "release_date" looks like "2010-07-16" — we only want the year ([:4])
        # If there's no release date, we show "N/A"
        year = movie.get("release_date", "N/A")[:4]

        # "vote_average" is the TMDB rating out of 10
        rating = movie.get("vote_average", "N/A")

        # "id" is the unique TMDB identifier — we'll need this later
        movie_id = movie.get("id")

        print(f"{i}. {title} ({year}) — ⭐ {rating} — ID: {movie_id}")

    print("-" * 40)


# This block runs only when you execute main.py directly
if __name__ == "__main__":
    connect_to_api()

    # Ask the user to type a movie title
    query = input("\n🔍 Search for a movie: ")

    # Call the search function from tmdb.py
    results = search_movie(query)

    # Display the results
    display_search_results(results)