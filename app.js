const addBtn = document.getElementById('add-btn');
const modal = document.getElementById('modal');
const modalClose = document.getElementById('modal-close');

addBtn.addEventListener('click', () => {
  modal.classList.add('open');
  document.getElementById('modal-input').focus();
});

modalClose.addEventListener('click', () => {
  modal.classList.remove('open');
});

modal.addEventListener('click', (e) => {
  if (e.target === modal) modal.classList.remove('open');
});

// ---------- Search inside the modal (issue #11) ----------

// Address of our Flask server. The browser talks to Flask,
// and Flask talks to TMDB, so the API key never reaches the browser.
const API_URL = 'http://127.0.0.1:5000';

const modalInput = document.getElementById('modal-input');
const modalResults = document.getElementById('modal-results');

// Stores the pending search so we can cancel it if the user keeps typing
let searchTimeout;

modalInput.addEventListener('input', () => {
  // Cancel the previous search: the user is still typing
  clearTimeout(searchTimeout);

  const query = modalInput.value.trim();

  // Empty field: clear the list and stop here
  if (query === '') {
    modalResults.innerHTML = '';
    return;
  }

  // Only search after 400 ms without typing (this is called "debounce")
  searchTimeout = setTimeout(() => searchMovies(query), 400);
});

async function searchMovies(query) {
  try {
    // encodeURIComponent handles spaces and accents in the title
    const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
    const movies = await response.json();
    renderResults(movies);
  } catch (error) {
    // Happens when the Flask server is not running
    modalResults.innerHTML = '<li>Could not reach the server.</li>';
  }
}

function renderResults(movies) {
  modalResults.innerHTML = '';

  if (movies.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'No films found.';
    modalResults.appendChild(li);
    return;
  }

  movies.forEach((movie) => {
    const li = document.createElement('li');
    // Some films have no release date, so year can be empty
    li.textContent = `${movie.title} (${movie.year || '—'})`;

    // Clicking a result adds that film to the history
    li.addEventListener('click', () => addToHistory(movie, li));

    modalResults.appendChild(li);
  });

  movies.forEach((movie) => {
    const li = document.createElement('li');
    // Some films have no release date, so year can be empty
    li.textContent = `${movie.title} (${movie.year || '—'})`;
    modalResults.appendChild(li);
  });
}

async function addToHistory(movie, li) {
  try {
    const response = await fetch(`${API_URL}/history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(movie)
    });

    if (response.status === 201) {
      // Added: close the modal and reset it for next time
      modal.classList.remove('open');
      modalInput.value = '';
      modalResults.innerHTML = '';
    } else if (response.status === 409) {
      // Duplicate: tell the user right on the clicked line
      li.textContent = `${movie.title} - already in your history`;
    } else {
      li.textContent = 'Something went wrong. Try again.';
    }
  } catch (error) {
    li.textContent = 'Could not reach the server.';
  }
}