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
def post_history():
    movie = request.get_json()
    add_to_history(movie)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)