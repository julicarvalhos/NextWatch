# app.py
#
# The Flask server: the bridge between the web page and the rest of the app.
#
#   browser (app.js)  --->  app.py  --->  tmdb.py     ---> TMDB API
#                                   --->  history.py  ---> history.json
#
# The browser never talks to TMDB directly. That keeps the API key
# on the server, where visitors can't see it.
#
# Routes:
#   GET  /search?q=<title>   search TMDB, returns up to 5 movies
#   GET  /history            the full watch history
#   POST /history            add one movie to the history
#
# Run with: python app.py   (then the API lives at http://127.0.0.1:5000)

from flask import Flask, jsonify, request
from flask_cors import CORS
from tmdb import search_movie
from history import load_history, add_to_history

app = Flask(__name__)

# Browsers block a page from calling a server on a different origin
# (here: index.html opened as a file vs. the API on 127.0.0.1:5000).
# CORS tells the browser this server accepts those calls.
CORS(app)

@app.route('/search')
def search():
    """
    Searches TMDB by title for the modal in the web page.

    Query string:
        q: the title typed by the user, e.g. /search?q=amadeus

    Returns:
        JSON list with up to 5 movies, each with
        id, title, year, rating and poster.
    """

    # request.args holds the query string; '' if "q" wasn't sent
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    results = search_movie(query)

    # TMDB returns ~20 movies with many fields each. The modal only
    # shows 5, so we keep just those and only the fields the page uses.
    movies = []
    for movie in results[:5]:
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title", "Unknown"),
            # "2010-07-16"[:4] -> "2010". Some films have release_date "",
            # which gives "" here, so the page shows "—" instead.
            "year": movie.get("release_date", "N/A")[:4],
            "rating": movie.get("vote_average", "N/A"),
            # Only the end of the image path, e.g. "/gQRf...jpg", or None.
            # The page must add TMDB's image address in front to show it.
            "poster": movie.get("poster_path")
        })

    # jsonify turns the Python list into a JSON response
    return jsonify(movies)

@app.route('/history')
def get_history():
    """Returns the whole watch history as a JSON list."""
    return jsonify(load_history())

@app.route('/history', methods=['POST'])
def post_history():
    """
    Adds a movie to the watch history.

    Expects a JSON body with at least "id" and "title"
    (the page sends one of the movies returned by /search).

    Returns:
        201 {"status": "added"}      the movie was saved
        400 {"error": ...}           the body was missing or incomplete
        409 {"status": "duplicate"}  the movie was already in the history
    """

    # silent=True returns None instead of crashing if the body isn't valid JSON
    movie = request.get_json(silent=True)

    if not movie or "id" not in movie or "title" not in movie:
        return jsonify({"error": "Movie must have an id and a title"}), 400

    # Copy only the fields we use, so the client can't fill
    # history.json with anything else it decides to send
    movie_to_save = {
        "id": movie["id"],
        "title": movie["title"],
        "year": movie.get("year", ""),
        "rating": movie.get("rating"),
        "poster": movie.get("poster")
    }

    # add_to_history returns False for duplicates (see history.py)
    added = add_to_history(movie_to_save)

    if not added:
        return jsonify({"status": "duplicate"}), 409

    return jsonify({"status": "added"}), 201

# Only runs when the file is executed directly (python app.py),
# not when another file imports it.
# debug=True restarts the server on every save and shows detailed errors.
# It's only for development: never leave it on in a public server.
if __name__ == '__main__':
    app.run(debug=True)