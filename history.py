# history.py
# This file handles everything related to the user's watch history.
# It saves and loads data from a local JSON file called history.json.

import json
import os

# The name of the file where we'll store the watch history
# Using a constant makes it easy to change the filename later if needed
HISTORY_FILE = "history.json"


def load_history():
    """
    Loads the watch history from the JSON file.

    Returns:
        list: A list of movie dictionaries the user has watched.
              Returns an empty list if the file doesn't exist yet.
    """

    # Check if the file exists before trying to open it
    # On the very first run, it won't exist yet — that's normal
    if not os.path.exists(HISTORY_FILE):
        return []

    # Open the file in read mode ("r") and parse the JSON into a Python list
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    """
    Saves the current watch history to the JSON file.

    Parameters:
        history (list): The full list of watched movie dictionaries to save
    """

    # Open the file in write mode ("w") — this overwrites the file completely
    # indent=4 makes the JSON human-readable with proper indentation
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def add_to_history(movie):
    """
    Adds a single movie to the watch history, avoiding duplicates.

    Parameters:
        movie (dict): A dictionary with at least "id" and "title" keys

    Returns:
        bool: True if the movie was added, False if it was already in history
    """

    # Load the current history from the file first
    history = load_history()

    # Check if this movie is already in the history by comparing TMDB IDs
    # We use any() to loop through and check — it stops as soon as it finds a match
    already_watched = any(m["id"] == movie["id"] for m in history)

    if already_watched:
        print(f"⚠️  '{movie['title']}' is already in your watch history.")
        return False

    # Add the new movie to the list
    history.append(movie)

    # Save the updated list back to the file
    save_history(history)

    print(f"✅ '{movie['title']}' added to your watch history!")
    return True


def remove_from_history(movie_id):
    """
    Removes a movie from the watch history by its TMDB ID.

    Parameters:
        movie_id (int): The TMDB ID of the movie to remove

    Returns:
        bool: True if removed successfully, False if not found
    """

    history = load_history()

    # Build a new list that excludes the movie with the matching ID
    # This is cleaner than finding the index and using .pop()
    updated_history = [m for m in history if m["id"] != movie_id]

    # If the lengths are the same, nothing was removed — movie wasn't found
    if len(updated_history) == len(history):
        print("❌ Movie not found in history.")
        return False

    save_history(updated_history)
    print("✅ Movie removed from watch history.")
    return True