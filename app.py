from flask import Flask, jsonify, request
from flask_cors import CORS
from tmdb import search_movie
from history import load_history, add_to_history

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = search_movie(query)
    movies = []
    for movie in results[:5]:
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title", "Unknown"),
            "year": movie.get("release_date", "N/A")[:4],
            "rating": movie.get("vote_average", "N/A"),
            "poster": movie.get("poster_path")
        })
    return jsonify(movies)

@app.route('/history')
def get_history():
    return jsonify(load_history())

@app.route('/history', methods=['POST'])
@app.route('/history', methods=['POST'])
def post_history():
    # silent=True returns None instead of crashing if the body isn't valid JSON
    movie = request.get_json(silent=True)

    # Reject requests missing the fields we need (400 = Bad Request)
    if not movie or "id" not in movie or "title" not in movie:
        return jsonify({"error": "Movie must have an id and a title"}), 400

    # Save only the fields we use, now including the poster
    movie_to_save = {
        "id": movie["id"],
        "title": movie["title"],
        "year": movie.get("year", ""),
        "rating": movie.get("rating"),
        "poster": movie.get("poster")
    }

    # add_to_history returns False when the movie is already there
    added = add_to_history(movie_to_save)

    if not added:
        # 409 = Conflict: the movie already exists
        return jsonify({"status": "duplicate"}), 409

    # 201 = Created
    return jsonify({"status": "added"}), 201

if __name__ == '__main__':
    app.run(debug=True)