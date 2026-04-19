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

for (const btn of document.querySelectorAll('.print-btn')) {
  btn.addEventListener('click', () => window.print());
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

const abbrs = document.querySelectorAll('abbr[title]');
if (abbrs.length) {
  let popover = null;
  const hidePopover = () => {
    if (!popover) return;
    popover.remove();
    popover = null;
  };
  const showPopover = el => {
    hidePopover();
    const text = el.getAttribute('title');
    if (!text) return;
    popover = document.createElement('div');
    popover.className = 'abbr-pop';
    popover.setAttribute('role', 'tooltip');
    popover.textContent = text;
    document.body.appendChild(popover);
    const rect = el.getBoundingClientRect();
    const popRect = popover.getBoundingClientRect();
    const maxLeft = window.innerWidth - popRect.width - 8;
    const left = Math.max(8, Math.min(maxLeft, rect.left + window.scrollX));
    const spaceBelow = window.innerHeight - rect.bottom;
    const showAbove = spaceBelow < popRect.height + 16 && rect.top > popRect.height + 16;
    const top = showAbove
      ? rect.top + window.scrollY - popRect.height - 6
      : rect.bottom + window.scrollY + 6;
    popover.style.left = left + 'px';
    popover.style.top = top + 'px';
  };
  for (const a of abbrs) a.tabIndex = 0;
  document.addEventListener('click', event => {
    const target = event.target.closest('abbr[title]');
    if (target) {
      event.preventDefault();
      popover?.contains(event.target) ? hidePopover() : showPopover(target);
      return;
    }
    if (popover && !event.target.closest('.abbr-pop')) hidePopover();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') hidePopover();
    else if (event.key === 'Enter' && event.target.matches('abbr[title]')) {
      event.preventDefault();
      showPopover(event.target);
    }
  });
  window.addEventListener('scroll', hidePopover, true);
  window.addEventListener('resize', hidePopover);
}

if (location.hash) {
  const target = document.getElementById(location.hash.slice(1));
  if (target?.tagName === 'DETAILS') target.open = true;
}

const detailsNodes = [...document.querySelectorAll('details')];
const savedOpenState = new WeakMap();
const expandAllDetails = () => {
  for (const d of detailsNodes) {
    savedOpenState.set(d, d.open);
    d.open = true;
  }
};
const restoreDetails = () => {
  for (const d of detailsNodes) {
    if (savedOpenState.has(d)) d.open = savedOpenState.get(d);
  }
};
window.addEventListener('beforeprint', expandAllDetails);
window.addEventListener('afterprint', restoreDetails);
const printMedia = matchMedia('print');
printMedia.addEventListener('change', event => {
  event.matches ? expandAllDetails() : restoreDetails();
});
