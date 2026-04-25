# NextWatch

NextWatch is a movie recommendation helper that combines a TMDB-powered search backend with a simple watch history workflow. It lets you search for films, save favorites locally, and explore a polished UI prototype built with HTML, CSS, and JavaScript.

## Screenshot

![NextWatch screenshot](add ss here)

> Add a `screenshot.png` file to the repository root to show the app running here.

## Technologies Used

- Python 3
- TMDB API
- Requests library
- HTML5
- CSS3
- JavaScript

## What it does

NextWatch provides a lightweight movie search experience using The Movie Database (TMDB). It includes:

- TMDB movie search via `tmdb.py`
- Local watch history persistence using `history.json`
- A simple CLI flow in `main.py`
- A static browser UI template in `index.html`, `style.css`, and `app.js`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NextWatch.git
   cd NextWatch-main
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install requests
   ```
4. Create a `config.py` file in the project root with your TMDB API key:
   ```python
   API_KEY = "your_tmdb_api_key_here"
   ```
5. Run the app:
   ```bash
   python main.py
   ```

## How to Use

1. Run `python main.py`.
2. When prompted, type the name of a movie to search.
3. The app will display the top results and automatically add the first result to your watch history.
4. After search, your saved watch history will be printed from `history.json`.

## TMDB API Key Setup

This project uses The Movie Database API for searching film data. To use it:

1. Create or sign in to your account at https://www.themoviedb.org/.
2. Go to your account settings, then `API`.
3. Request a developer API key.
4. Add the key to a new `config.py` file in the repo root:
   ```python
   API_KEY = "your_tmdb_api_key_here"
   ```

### Important

- Keep your TMDB API key private.
- Do not commit `config.py` or your API key to version control.

## Project Structure

- `index.html` — static frontend layout
- `style.css` — UI styling
- `app.js` — frontend interaction logic
- `main.py` — CLI entry point and app flow
- `tmdb.py` — TMDB search and movie detail helper functions
- `history.py` — local watch history storage
- `history.json` — saved watch history file
- `config.py` — local TMDB API key configuration (not included)

## Notes

- The frontend UI is currently a static prototype and is not directly integrated with the Python backend.
- `history.json` is generated automatically after the first successful search.
- If you want to enhance the project, consider connecting the browser UI to the Python backend or adding selection support for search results.


