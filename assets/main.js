const root = document.documentElement;

const readStoredTheme = () => {
  try { return localStorage.getItem('theme'); } catch { return null; }
};
const writeStoredTheme = value => {
  try { localStorage.setItem('theme', value); } catch {}
};

const stored = readStoredTheme();
if (stored === 'light' || stored === 'dark') root.dataset.theme = stored;

const currentTheme = () => root.dataset.theme
  ?? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

const THEME_LABELS = {
  fr: { toLight: 'Passer en mode clair', toDark: 'Passer en mode sombre' },
  en: { toLight: 'Switch to light mode', toDark: 'Switch to dark mode' },
};
const pageLang = () => (root.lang || 'fr').startsWith('en') ? 'en' : 'fr';

const paintThemeToggle = (btn, theme) => {
  const labels = THEME_LABELS[pageLang()];
  btn.textContent = theme === 'dark' ? '☀' : '☾';
  const label = theme === 'dark' ? labels.toLight : labels.toDark;
  btn.setAttribute('aria-label', label);
  btn.setAttribute('title', label);
};

const themeToggle = document.querySelector('.theme-toggle');
if (themeToggle) {
  paintThemeToggle(themeToggle, currentTheme());
  themeToggle.addEventListener('click', () => {
    const next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    writeStoredTheme(next);
    paintThemeToggle(themeToggle, next);
  });
}

const backLink = document.querySelector('[data-action="back"]');
if (backLink) {
  backLink.addEventListener('click', event => {
    const sameOriginReferrer = document.referrer
      && new URL(document.referrer, location.href).origin === location.origin;
    if (history.length > 1 && sameOriginReferrer) {
      event.preventDefault();
      history.back();
    }
  });
}

const searchInput = document.querySelector('.search-input');
if (searchInput) {
  const cards = [...document.querySelectorAll('.need-card')];
  const emptyState = document.querySelector('.no-results');
  const normalise = text => text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  let scheduled = 0;
  const applyFilter = () => {
    const query = normalise(searchInput.value.trim());
    let visible = 0;
    for (const card of cards) {
      const match = !query || normalise(card.textContent).includes(query);
      card.hidden = !match;
      if (match) visible += 1;
    }
    if (emptyState) emptyState.hidden = visible > 0 || !query;
  };

  searchInput.addEventListener('input', () => {
    cancelAnimationFrame(scheduled);
    scheduled = requestAnimationFrame(applyFilter);
  });
  searchInput.addEventListener('keydown', event => {
    if (event.key === 'Escape' && searchInput.value) {
      searchInput.value = '';
      applyFilter();
    }
  });
}

if (location.hash) {
  const target = document.getElementById(location.hash.slice(1));
  if (target?.tagName === 'DETAILS') target.open = true;
}
