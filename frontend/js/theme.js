/* ============================================================
   THEME TOGGLE WITH LOCALSTORAGE
   ============================================================ */
const themeToggle = document.getElementById('themeToggle');
const themeIcon   = themeToggle.querySelector('i');
const htmlEl      = document.documentElement;

// On page load: Restore saved theme
if (localStorage.getItem('theme') === 'light') {
  htmlEl.setAttribute('data-theme', 'light');
  themeIcon.className = 'fas fa-sun';
}

themeToggle.addEventListener('click', () => {
  const isLight = htmlEl.getAttribute('data-theme') === 'light';

  if (!isLight) {
    htmlEl.setAttribute('data-theme', 'light');
    themeIcon.className = 'fas fa-sun';
    localStorage.setItem('theme', 'light');
  } else {
    htmlEl.removeAttribute('data-theme');
    themeIcon.className = 'fas fa-moon';
    localStorage.setItem('theme', 'dark');
  }
});