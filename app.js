// app.js
//
// Runs in the browser and makes index.html interactive.
//
// It never talks to TMDB directly: every request goes to our Flask
// server (app.py), which keeps the API key out of the browser.
//
//   app.js  --fetch-->  app.py (http://127.0.0.1:5000)
//
// Sections:
//   1. Opening and closing the "add a film" modal
//   2. Searching as the user types (issue #11)
//   3. Adding the clicked film to the history (issue #11)
//   4. Showing and removing films in the history strip (issue #12)


// ---------- 1. Modal open / close ----------

// Grab the elements once and reuse them, instead of searching the page every time
const addBtn = document.getElementById('add-btn');
const modal = document.getElementById('modal');
const modalClose = document.getElementById('modal-close');

// The modal is hidden by CSS until it has the "open" class (see style.css)
addBtn.addEventListener('click', () => {
  modal.classList.add('open');
  // Put the cursor in the search field so the user can type right away
  document.getElementById('modal-input').focus();
});

modalClose.addEventListener('click', () => {
  modal.classList.remove('open');
});

// Clicking the dark area around the box also closes the modal.
// e.target is the element actually clicked: if it's the overlay itself
// (and not the box or something inside it), the click was outside the box.
modal.addEventListener('click', (e) => {
  if (e.target === modal) modal.classList.remove('open');
});

// ---------- 2. Search inside the modal ----------

// Address of our Flask server (must be running: python app.py)
const API_URL = 'http://127.0.0.1:5000';

const modalInput = document.getElementById('modal-input');
const modalResults = document.getElementById('modal-results');

// Holds the search that is waiting to run, so it can be cancelled

let searchTimeout;

// "input" fires on every change to the field: typing, deleting, pasting
modalInput.addEventListener('input', () => {
  // The user typed again, so the previously scheduled search is outdated
  clearTimeout(searchTimeout);

  const query = modalInput.value.trim();

  if (query === '') {
    modalResults.innerHTML = '';
    return;
  }

  // Debounce: wait until the user stops typing for 400 ms before searching.
  // Without it, typing "amadeus" would send 7 requests, one per letter.
  searchTimeout = setTimeout(() => searchMovies(query), 400);
});

/**
 * Asks the Flask server for movies matching the query
 * and shows them in the modal.
 *
 * async/await lets us wait for the server's answer
 * without freezing the page in the meantime.
 */
async function searchMovies(query) {
  try {
    // encodeURIComponent escapes spaces and accents: "o poderoso" -> "o%20poderoso"
    const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
    // Turns the JSON text sent by app.py into a JavaScript array
    const movies = await response.json();
    renderResults(movies);
  } catch (error) {
    // fetch only throws when it can't reach the server at all,
    // which almost always means app.py isn't running
    modalResults.innerHTML = '<li>Could not reach the server.</li>';
  }
}

/**
 * Replaces the modal list with one clickable <li> per movie.
 *
 * @param {Array} movies - movies from /search: { id, title, year, rating, poster }
 */
function renderResults(movies) {
  // Clear the results of the previous search
  modalResults.innerHTML = '';

  if (movies.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'No films found.';
    modalResults.appendChild(li);
    return;
  }

  movies.forEach((movie) => {
    const li = document.createElement('li');
    // textContent (not innerHTML) shows the title as plain text,
    // so a title containing HTML can't inject code into the page.
    // year is "" for films without a release date, so we show "—".
    li.textContent = `${movie.title} (${movie.year || '—'})`;

    // Each <li> remembers its own movie, so the click knows what to add
    li.addEventListener('click', () => addToHistory(movie, li));

    modalResults.appendChild(li);
  });
}

// ---------- 3. Add to history ----------

/**
 * Sends a movie to POST /history and reacts to the server's answer.
 *
 * @param {Object} movie - the movie that was clicked (same shape as /search returns)
 * @param {HTMLElement} li - the clicked line, used to show messages in place
 */
async function addToHistory(movie, li) {
  try {
    const response = await fetch(`${API_URL}/history`, {
      method: 'POST',
      // Tells Flask the body is JSON, so request.get_json() can read it
      headers: { 'Content-Type': 'application/json' },
      // fetch sends text, so the object is converted to a JSON string
      body: JSON.stringify(movie)
    });

    // The status codes come from post_history() in app.py
    if (response.status === 201) {
      // Added: close and reset the modal for the next search
      modal.classList.remove('open');
      modalInput.value = '';
      modalResults.innerHTML = '';
      // Redraw the strip so the new film shows up right away
      loadHistory();
    } else if (response.status === 409) {
      // Duplicate: keep the modal open and explain on the clicked line
      li.textContent = `${movie.title} - already in your history`;
    } else {
      // 400 or anything unexpected
      li.textContent = 'Something went wrong. Try again.';
    }
  } catch (error) {
    li.textContent = 'Could not reach the server.';
  }
}

// ---------- 4. Watch history strip (issue #12) ----------

// TMDB only sends the end of the image path ("/gQRf...jpg").
// This is the start of it. w185 means 185px wide: enough for
// small thumbnails, even on sharp screens.
const IMAGE_URL = 'https://image.tmdb.org/t/p/w185';

const historyList = document.getElementById('history-list');

/**
 * Fetches the watch history from the server and draws it.
 * Runs when the page opens and again after a film is added.
 */
async function loadHistory() {
  try {
    const response = await fetch(`${API_URL}/history`);
    const history = await response.json();
    renderHistory(history);
  } catch (error) {
    historyList.textContent = 'Could not load your history.';
  }
}

/**
 * Replaces the history strip with one thumbnail per film.
 *
 * @param {Array} history - films from /history: { id, title, year, rating, poster }
 */
function renderHistory(history) {
  historyList.innerHTML = '';

  history.forEach((movie) => {
    // <div class="thumb"> holds the image and the title (styles in style.css)
    const thumb = document.createElement('div');
    thumb.className = 'thumb';
    // Full title on hover (long ones get cut with "…") and a hint of what clicking does
    thumb.title = `${movie.title} (${movie.year || '—'}) — click to remove`;

    if (movie.poster) {
      const img = document.createElement('img');
      img.src = IMAGE_URL + movie.poster;
      // alt is read by screen readers and shown if the image fails to load
      img.alt = movie.title;
      thumb.appendChild(img);
    } else {
      // Older entries and some films have no poster: show an empty frame instead
      const empty = document.createElement('div');
      empty.className = 'thumb-empty';
      thumb.appendChild(empty);
    }

    const name = document.createElement('p');
    name.className = 'thumb-name';
    name.textContent = movie.title;
    thumb.appendChild(name);

    thumb.addEventListener('click', () => removeFromHistory(movie));    
    historyList.appendChild(thumb);
  });
}

/**
 * Asks for confirmation, removes the film on the server and redraws the strip.
 *
 * @param {Object} movie - the film whose thumbnail was clicked
 */
async function removeFromHistory(movie) {
  // A single misclick would delete the film, so ask first.
  // confirm() shows the browser's OK/Cancel box and returns true or false.
  if (!confirm(`Remove "${movie.title}" from your history?`)) return;

  try {
    const response = await fetch(`${API_URL}/history/${movie.id}`, { method: 'DELETE' });

    // response.ok is true for any 2xx status (here: 200)
    if (!response.ok) {
      alert('Could not remove this film. Try again.');
    }
  } catch (error) {
    alert('Could not reach the server.');
  }

  // Redraw in every case, so the strip always matches history.json
  loadHistory();
}

// Draw the history as soon as the page opens
loadHistory();