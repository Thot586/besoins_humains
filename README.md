# Besoins humains fondamentaux

Guide interactif bilingue (FR/EN) sur les neuf besoins humains fondamentaux selon la taxonomie de Manfred Max-Neef (1991).

Auteur : **Dr FENOHASINA T.J. Felicien** — Psychiatre.

## Structure

```
├── index.html                  Page d'accueil (FR)
├── references.html             Sources et méthodologie (FR)
├── besoins/                    9 pages besoin (FR)
├── en/
│   ├── index.html              Home (EN)
│   ├── references.html         Sources and methodology (EN)
│   └── needs/                  9 need pages (EN)
├── assets/
│   ├── styles.css              Design system
│   ├── fonts.css               @font-face locaux
│   ├── fonts/                  WOFF2 auto-hébergés
│   ├── main.js                 Module ES — thème, recherche, navigation
│   └── favicon.svg
├── sitemap.xml
├── robots.txt
└── set_base_url.py             Reconfigure le domaine de déploiement
```

## Utilisation locale

Servir localement (aucun build requis) :
```bash
python -m http.server 8000
```
Puis ouvrir http://localhost:8000

## Déploiement

Déposer le dossier tel quel sur un hébergeur statique (GitHub Pages, Netlify, Cloudflare Pages, OVH, etc.). Avant le premier déploiement, configurer le domaine final :

```bash
python set_base_url.py https://votre-domaine.fr
```

Cette commande met à jour `sitemap.xml`, `robots.txt`, et les balises `<link rel="alternate" hreflang>` dans les 22 pages HTML.

## Caractéristiques techniques

- HTML sémantique + ARIA pour l'accessibilité (WCAG AA)
- Lighthouse 100/100/100 (Accessibility, Best Practices, SEO)
- Zéro dépendance externe, zéro build, zéro tracker
- Polices auto-hébergées (Fraunces, Inter, JetBrains Mono) en WOFF2
- Bascule FR ↔ EN + clair/sombre (persistée en localStorage)
- `@media print` soigné pour export PDF lecteur
- Module JavaScript ES6+ (`<script type="module">`)

## Licence

Contenu pédagogique. Auteur : Dr FENOHASINA T.J. Felicien.
