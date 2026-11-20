# main.py
#
# Terminal version of NextWatch: the first prototype of the app.
#
# It was used to build and test the core logic (tmdb.py and history.py)
# before the web interface existed. The real app is now the web version:
# app.py (Flask server) + index.html / app.js (page).
#
# What it does when run (python main.py):
#   1. checks that the TMDB API key works
#   2. asks for a movie title and shows the top 5 results
#   3. saves the FIRST result to the history (no choice, see handle_search)
#   4. prints the whole history
#
# It writes to the same history.json as the web app.

import requests
from config import API_KEY
from tmdb import search_movie, REQUEST_TIMEOUT
from history import add_to_history, load_history

# Same address as in tmdb.py. Duplicated here only for connect_to_api().
BASE_URL = "https://api.themoviedb.org/3"


def connect_to_api():
    """
    Checks that TMDB is reachable and the API key is valid.

    Calls /configuration, a lightweight endpoint, just to see if the
    request succeeds. A 401 status here almost always means a wrong key
    in config.py.
    """

    url = f"{BASE_URL}/configuration"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as error:
        print(f"Could not reach TMDB: {error}")
        return
    if response.status_code == 200:
        print("Connected to TMDB API successfully!")
    else:
        print(f"Connection failed. Status code: {response.status_code}")


def display_search_results(movies):
    """
    Prints up to 5 movies as a numbered list.

    Parameters:
        movies (list): Movies in TMDB's raw format, as returned by search_movie()
    """

    if not movies:
        print("No movies found.")
        return

    print("\nSearch Results:")
    print("-" * 40)

    # enumerate(..., start=1) numbers the list from 1 instead of 0
    for i, movie in enumerate(movies[:5], start=1):
        title = movie.get("title", "Unknown Title")
        # "2010-07-16"[:4] -> "2010"
        year = movie.get("release_date", "N/A")[:4]
        rating = movie.get("vote_average", "N/A")
        movie_id = movie.get("id")

        print(f"{i}. {title} ({year}) — ⭐ {rating} — ID: {movie_id}")

    print("-" * 40)


def display_history():
    """
    Prints every movie in the watch history, or a message if it's empty.
    """

    history = load_history()

    print("\nYour watch history:")
    print("-" * 40)

    if not history:
        print("  No movies yet.")
    else:
        for i, movie in enumerate(history, start=1):
            print(f"{i}. {movie['title']} ({movie['year']}) — ⭐ {movie['rating']}")

    print("-" * 40)


def handle_search():
    """
    Asks for a title, shows the results and saves the first one to the history.

    Always saving the first result was a shortcut to test history.py.
    Choosing among the results was planned for the terminal (issue #5),
    but it was done in the web modal instead (issue #11).
    """

    query = input("\nSearch for a movie: ")
    results = search_movie(query)
    display_search_results(results)

    if results:
        first = results[0]

        # Keep only the fields the history uses, not TMDB's whole response.
        # Unlike the web app, this doesn't save the poster.
        movie_to_save = {
            "id": first["id"],
            "title": first.get("title", "Unknown"),
            "year": first.get("release_date", "N/A")[:4],
            "rating": first.get("vote_average", "N/A")
        }

        add_to_history(movie_to_save)


# Only runs when the file is executed directly (python main.py),
# not when another file imports it
if __name__ == "__main__":
    connect_to_api()
    handle_search()
    display_history()