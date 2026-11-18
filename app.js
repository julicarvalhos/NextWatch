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