"""Static site generator for Guide Pratique Besoins Humains.

Reads src/pages.json (manifest) and src/body/<file>.html (page bodies),
assembles the shared shell (head, header, breadcrumb, footer) around each
body, and writes the result to the `out` path declared in the manifest.

Usage:
    python scripts/build.py
"""
from __future__ import annotations

import json
import pathlib
import posixpath
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

# --- Configuration ---------------------------------------------------------

BASE_URL = 'https://example.com'  # kept in sync by scripts/set_base_url.py
AUTHOR_FR = 'Dr FENOHASINA T.J. Felicien — Psychiatre'
AUTHOR_EN = 'Dr FENOHASINA T.J. Felicien — Psychiatrist'

# FR slug -> EN slug mapping (paired pages).
SLUG_PAIRS_FR_EN = {
    'index': 'index',
    'references': 'references',
    'subsistance': 'subsistence',
    'protection': 'protection',
    'affection': 'affection',
    'comprehension': 'understanding',
    'participation': 'participation',
    'loisir': 'leisure',
    'creation': 'creation',
    'identite': 'identity',
    'liberte': 'freedom',
}

L10N = {
    'fr': {
        'site_title': 'Besoins humains fondamentaux',
        'skip': 'Aller au contenu',
        'theme_label': 'Changer de thème',
        'lang_nav_label': 'Langue',
        'back': 'Retour',
        'home': 'Accueil',
        'print': 'Imprimer',
        'print_label': 'Imprimer cette page',
        'bc_label': 'Navigation',
        'refs_link': 'Références',
        'home_link': 'Accueil',
        'author': AUTHOR_FR,
        'safety_html': (
            "Ce guide est une boussole, pas un diagnostic. "
            "Si vous traversez une période difficile, parlez-en à un professionnel. "
            "En France&nbsp;: <strong>3114</strong> (prévention du suicide, 24/7, gratuit)."
        ),
    },
    'en': {
        'site_title': 'Fundamental human needs',
        'skip': 'Skip to content',
        'theme_label': 'Toggle theme',
        'lang_nav_label': 'Language',
        'back': 'Back',
        'home': 'Home',
        'print': 'Print',
        'print_label': 'Print this page',
        'bc_label': 'Navigation',
        'refs_link': 'References',
        'home_link': 'Home',
        'author': AUTHOR_EN,
        'safety_html': (
            "This guide is a compass, not a diagnosis. "
            "If you are going through a difficult time, "
            "reach out to a professional or a crisis line in your country."
        ),
    },
}

LANG_GLYPH_SVG = (
    '<svg class="lang-glyph" aria-hidden="true" viewBox="0 0 16 16" '
    'width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.3">'
    '<circle cx="8" cy="8" r="6.5"/>'
    '<ellipse cx="8" cy="8" rx="3" ry="6.5"/>'
    '<path d="M1.5 8h13"/></svg>'
)

THEME_MOON_SVG = (
    '<svg class="theme-glyph theme-glyph-moon" aria-hidden="true" viewBox="0 0 16 16" '
    'width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.3" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M13.5 9.5A5.5 5.5 0 1 1 6.5 2.5a4.5 4.5 0 0 0 7 7z"/></svg>'
)

THEME_SUN_SVG = (
    '<svg class="theme-glyph theme-glyph-sun" aria-hidden="true" viewBox="0 0 16 16" '
    'width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.3" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="8" cy="8" r="3"/>'
    '<path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3.05 3.05l1.06 1.06'
    'M11.89 11.89l1.06 1.06M3.05 12.95l1.06-1.06M11.89 4.11l1.06-1.06"/></svg>'
)

ANTI_FLASH_SCRIPT = (
    "<script>\n"
    "(function(){try{var t=localStorage.getItem('theme');"
    "if(t==='light'||t==='dark')document.documentElement.dataset.theme=t;}"
    "catch(e){}})();\n"
    "</script>"
)

# --- Helpers ---------------------------------------------------------------


def pair_key(slug: str, lang: str) -> str:
    """Return a language-agnostic key identifying a paired page."""
    if lang == 'fr':
        return slug
    fr_to_en = SLUG_PAIRS_FR_EN
    en_to_fr = {v: k for k, v in fr_to_en.items()}
    return en_to_fr.get(slug, slug)


def rel_from(from_path: str, to_path: str) -> str:
    """Relative posix path from from_path's directory to to_path."""
    from_dir = posixpath.dirname(from_path)
    return posixpath.relpath(to_path, from_dir or '.')


def prefix_for(out_path: str) -> str:
    """Returns '', '../', '../../' based on nesting depth of out_path.
    Used for asset paths (favicon, styles, main.js — all at the repo root)."""
    depth = len(pathlib.PurePosixPath(out_path).parts) - 1
    return '../' * depth


def lang_index_path(lang: str) -> str:
    """Path to the language's home page, relative to repo root."""
    return 'index.html' if lang == 'fr' else 'en/index.html'


def lang_refs_path(lang: str) -> str:
    """Path to the language's references page, relative to repo root."""
    return 'references.html' if lang == 'fr' else 'en/references.html'


def home_href(page: dict) -> str:
    return rel_from(page['out'], lang_index_path(page['lang']))


def refs_href(page: dict) -> str:
    return rel_from(page['out'], lang_refs_path(page['lang']))


# --- Shell templates -------------------------------------------------------


def canonical_url(out_path: str) -> str:
    """Canonical URL on BASE_URL.
    Root indexes collapse to pretty '/' and '/en/' forms."""
    if out_path == 'index.html':
        return BASE_URL + '/'
    if out_path == 'en/index.html':
        return BASE_URL + '/en/'
    return f'{BASE_URL}/{out_path}'


def fr_peer_out(page: dict, peer: dict) -> str:
    return page['out'] if page['lang'] == 'fr' else peer['out']


def en_peer_out(page: dict, peer: dict) -> str:
    return peer['out'] if page['lang'] == 'fr' else page['out']


def render_head(page: dict, prefix: str, alt_fr: str, alt_en: str) -> str:
    lang = page['lang']
    return '\n'.join([
        f'<html lang="{lang}">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
        '<meta name="color-scheme" content="light dark">',
        f'<meta name="description" content="{page["description"]}">',
        '<meta name="theme-color" content="#faf7f1" media="(prefers-color-scheme: light)">',
        '<meta name="theme-color" content="#14141a" media="(prefers-color-scheme: dark)">',
        f'<title>{page["title"]}</title>',
        f'<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">',
        f'<link rel="stylesheet" href="{prefix}assets/styles.css">',
        f'<link rel="alternate" hreflang="fr" href="{alt_fr}">',
        f'<link rel="alternate" hreflang="en" href="{alt_en}">',
        f'<link rel="alternate" hreflang="x-default" href="{alt_fr}">',
        ANTI_FLASH_SCRIPT,
        '</head>',
    ])


def render_header(page: dict, peer: dict) -> str:
    lang = page['lang']
    t = L10N[lang]

    self_href = posixpath.basename(page['out'])
    peer_href = rel_from(page['out'], peer['out'])

    is_index = page['slug'] == 'index'
    site_title_href = self_href if is_index else home_href(page)
    site_title_attrs = ' aria-current="page"' if is_index else ''

    def lang_link(href, code, is_current):
        cur = ' aria-current="page"' if is_current else ''
        return (
            f'<a href="{href}"{cur} lang="{code}" hreflang="{code}">'
            f'{LANG_GLYPH_SVG}{code.upper()}</a>'
        )

    if lang == 'fr':
        fr_link = lang_link(self_href, 'fr', True)
        en_link = lang_link(peer_href, 'en', False)
    else:
        fr_link = lang_link(peer_href, 'fr', False)
        en_link = lang_link(self_href, 'en', True)

    return (
        '  <header class="site-header">\n'
        f'    <a href="{site_title_href}" class="site-title"{site_title_attrs}>{t["site_title"]}</a>\n'
        '    <div class="header-controls">\n'
        f'      <nav class="lang-switch" aria-label="{t["lang_nav_label"]}">\n'
        f'        {fr_link}\n'
        f'        {en_link}\n'
        '      </nav>\n'
        f'      <button class="theme-toggle" type="button" aria-label="{t["theme_label"]}">'
        f'{THEME_MOON_SVG}{THEME_SUN_SVG}</button>\n'
        '    </div>\n'
        '  </header>'
    )


def render_breadcrumb(page: dict) -> str:
    t = L10N[page['lang']]
    home = home_href(page)
    return (
        f'  <nav class="breadcrumb" aria-label="{t["bc_label"]}">\n'
        f'    <a href="{home}" data-action="back">'
        f'<span class="arrow" aria-hidden="true">←</span>{t["back"]}</a>\n'
        f'    <a href="{home}">'
        f'<span class="arrow" aria-hidden="true">⌂</span>{t["home"]}</a>\n'
        f'    <button type="button" class="print-btn" aria-label="{t["print_label"]}">'
        f'<span class="arrow" aria-hidden="true">⎙</span>{t["print"]}</button>\n'
        '  </nav>'
    )


def render_footer(page: dict) -> str:
    t = L10N[page['lang']]
    slug = page['slug']
    home = home_href(page)
    refs = refs_href(page)

    if slug == 'references':
        links = f'<a href="{home}">{t["home_link"]}</a>'
    elif slug == 'index':
        links = f'<a href="{refs}">{t["refs_link"]}</a>'
    else:
        links = (
            f'<a href="{refs}">{t["refs_link"]}</a> '
            '<span class="sep">·</span> '
            f'<a href="{home}">{t["home_link"]}</a>'
        )

    return (
        '  <footer class="site-footer">\n'
        f'    <p class="author">{t["author"]}</p>\n'
        f'    <p class="safety">{t["safety_html"]}</p>\n'
        f'    <p>{links}</p>\n'
        '  </footer>'
    )


# --- Page assembly ---------------------------------------------------------


def render_page(page: dict, peer: dict) -> str:
    lang = page['lang']
    t = L10N[lang]
    prefix = prefix_for(page['out'])
    body_attrs = (' ' + page['body_attrs']) if page['body_attrs'] else ''

    body_file = SRC / 'body' / page['body']
    body = body_file.read_text(encoding='utf-8').rstrip() + '\n'

    alt_fr = canonical_url(fr_peer_out(page, peer))
    alt_en = canonical_url(en_peer_out(page, peer))

    parts = [
        '<!DOCTYPE html>',
        render_head(page, prefix, alt_fr, alt_en),
        f'<body{body_attrs}>',
        f'<a class="skip-link" href="#main">{t["skip"]}</a>',
        '',
        '<div class="container">',
        render_header(page, peer),
        '',
    ]
    if page['slug'] != 'index':
        parts.append(render_breadcrumb(page))
        parts.append('')

    parts.append('  <main id="main">')
    parts.append(body.rstrip())
    parts.append('  </main>')
    parts.append('')
    parts.append(render_footer(page))
    parts.append('</div>')
    parts.append('')
    parts.append(f'<script type="module" src="{prefix}assets/main.js"></script>')
    parts.append('</body>')
    parts.append('</html>')

    return '\n'.join(parts) + '\n'


def build(check_only: bool = False) -> int:
    pages = json.loads((SRC / 'pages.json').read_text(encoding='utf-8'))
    by_key = {(pair_key(p['slug'], p['lang']), p['lang']): p for p in pages}

    changed = 0
    for p in pages:
        key = pair_key(p['slug'], p['lang'])
        other_lang = 'en' if p['lang'] == 'fr' else 'fr'
        peer = by_key.get((key, other_lang))
        if peer is None:
            print(f'!! no peer for {p["out"]}', file=sys.stderr)
            continue

        html = render_page(p, peer)
        out_path = ROOT / p['out']
        existing = out_path.read_text(encoding='utf-8') if out_path.exists() else ''
        if existing == html:
            continue
        if check_only:
            print(f'DIFF {p["out"]}')
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding='utf-8')
            print(f'wrote {p["out"]}')
        changed += 1
    return changed


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = build(check_only=check)
    if check and n:
        sys.exit(1)
