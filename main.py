# main.py
# This is the main entry point of the application.
# It connects to the TMDB API, allows the user to search for movies,
# and saves/loads their watch history.

import requests
from config import API_KEY
from tmdb import search_movie
from history import add_to_history, load_history

# The base URL for every TMDB API request
BASE_URL = "https://api.themoviedb.org/3"


def connect_to_api():
    """
    Tests the connection to the TMDB API.
    We call this once at startup to make sure everything is working
    before the user tries to do anything.
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
    Prints the search results in a clean, numbered format.

    Parameters:
        movies (list): The list of movie dictionaries returned by search_movie()
    """

    if not movies:
        print("No movies found.")
        return

    print("\n🎬 Search Results:")
    print("-" * 40)

    # Only show the first 5 results to keep the output clean
    for i, movie in enumerate(movies[:5], start=1):
        title = movie.get("title", "Unknown Title")

        # release_date looks like "2010-07-16" — [:4] grabs just the year
        year = movie.get("release_date", "N/A")[:4]

        rating = movie.get("vote_average", "N/A")
        movie_id = movie.get("id")

        print(f"{i}. {title} ({year}) — ⭐ {rating} — ID: {movie_id}")

    print("-" * 40)


def display_history():
    """
    Loads and prints the user's watch history from history.json.
    """

    history = load_history()

    print("\n📋 Your watch history:")
    print("-" * 40)

    if not history:
        print("  No movies yet.")
    else:
        for i, movie in enumerate(history, start=1):
            print(f"{i}. {movie['title']} ({movie['year']}) — ⭐ {movie['rating']}")

    print("-" * 40)


def handle_search():
    """
    Asks the user for a movie title, searches TMDB,
    displays the results, and saves the first result to history as a test.

    NOTE: This is temporary — in Issue #5 we'll let the user
    pick which result to add instead of always saving the first one.
    """

    # Ask the user what to search for
    query = input("\n🔍 Search for a movie: ")

    # Call the search function from tmdb.py
    results = search_movie(query)

    # Show the results on screen
    display_search_results(results)

    # Temporarily save the first result to test the history system
    # This will be replaced with a proper selection menu in Issue #5
    if results:
        first = results[0]

        # Only store the fields we actually need — not the entire TMDB response
        movie_to_save = {
            "id": first["id"],
            "title": first.get("title", "Unknown"),
            "year": first.get("release_date", "N/A")[:4],
            "rating": first.get("vote_average", "N/A")
        }

        add_to_history(movie_to_save)


# This block only runs when we execute main.py directly
if __name__ == "__main__":

    # Step 1: verify API connection at startup
    connect_to_api()

    # Step 2: search for a movie and temporarily save the first result
    handle_search()

    # Step 3: display the full watch history
    display_history()