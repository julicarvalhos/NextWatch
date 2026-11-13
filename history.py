# history.py
#
# Stores the user's watch history in a local JSON file (history.json).
#
# The history is a list of movie dictionaries, each one with:
#   id, title, year, rating and poster (poster may be missing on older entries)
#
# There is no database: every function reads the whole file, changes the
# list in memory and writes the whole file back. This is simple and fine
# for one user with a few hundred movies.
#
# Used by app.py (the Flask routes) and main.py (the terminal version).

import json
import os

# NOTE: this path is relative to the folder the app is *run from*,
# not to this file. Running "python app.py" from another folder
# would create a separate, empty history.json there.
HISTORY_FILE = "history.json"


def load_history():
    """
    Loads the watch history from the JSON file.

    Returns:
        list: A list of movie dictionaries the user has watched.
              Returns an empty list if the file doesn't exist yet.
    """

    # On the very first run there is no file yet
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        # json.load turns the file's text into Python lists and dicts
        return json.load(file)


def save_history(history):
    """
    Writes the full watch history to history.json, replacing what was there.

    Parameters:
        history (list): The complete list of movies to save.
                        Anything not in this list is lost.
    """

    # "w" erases the file before writing, which is why callers must
    # always pass the *complete* list, never just the new movie
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def add_to_history(movie):
    """
    Adds one movie to the end of the history, unless it's already there.

    Used by POST /history in app.py, which turns the return value
    into the 201 (added) or 409 (duplicate) response.

    Parameters:
        movie (dict): A movie with at least "id" and "title"

    Returns:
        bool: True if it was added, False if it was a duplicate
    """

    history = load_history()

    # Duplicates are detected by TMDB id, not title: different films
    # can share a title (there are two "Amadeus" in the search results).
    # any() stops at the first match instead of checking the whole list.
    already_watched = any(m["id"] == movie["id"] for m in history)

    if already_watched:
        print(f"'{movie['title']}' is already in your watch history.")
        return False

    history.append(movie)

    save_history(history)

    print(f"'{movie['title']}' added to your watch history!")
    return True


def remove_from_history(movie_id):
    """
    Removes a movie from the history by its TMDB id.

    Not used by the web app yet: issue #12 will add a route for it.

    Parameters:
        movie_id (int): The TMDB id of the movie to remove

    Returns:
        bool: True if it was removed, False if it wasn't in the history
    """

    history = load_history()

    # Build a new list with every movie except the one to remove
    updated_history = [m for m in history if m["id"] != movie_id]

    # Same length means nothing was filtered out: the id wasn't there
    if len(updated_history) == len(history):
        print("Movie not found in history.")
        return False

    save_history(updated_history)
    print("Movie removed from watch history.")
    return True