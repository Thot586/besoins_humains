"""One-shot: extract <main> content from each existing HTML into src/body/
and write src/pages.json manifest."""
import re
import pathlib
import json
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
(SRC / 'body').mkdir(parents=True, exist_ok=True)


def page_key(rel: str):
    rel = rel.replace('\\', '/')
    if rel == 'index.html':
        return 'fr', 'index'
    if rel == 'references.html':
        return 'fr', 'references'
    if rel == 'en/index.html':
        return 'en', 'index'
    if rel == 'en/references.html':
        return 'en', 'references'
    m = re.match(r'besoins/([a-z]+)\.html$', rel)
    if m:
        return 'fr', m.group(1)
    m = re.match(r'en/needs/([a-z]+)\.html$', rel)
    if m:
        return 'en', m.group(1)
    return None


def main():
    pages = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT).as_posix()
        key = page_key(rel)
        if not key:
            continue
        lang, slug = key
        text = p.read_text(encoding='utf-8')

        m = re.search(r'<main id="main">\n?(.*?)\n?  </main>', text, re.DOTALL)
        if not m:
            print(f'!! no main in {rel}', file=sys.stderr)
            continue
        main_body = m.group(1)

        m2 = re.search(r'<body([^>]*)>', text)
        body_attrs = m2.group(1).strip() if m2 else ''
        title = re.search(r'<title>([^<]+)</title>', text).group(1)
        desc = re.search(r'<meta name="description" content="([^"]+)"', text).group(1)

        body_filename = f'{lang}_{slug}.html'
        (SRC / 'body' / body_filename).write_text(main_body + '\n', encoding='utf-8')

        pages.append({
            'slug': slug,
            'lang': lang,
            'out': rel,
            'body': body_filename,
            'title': title,
            'description': desc,
            'body_attrs': body_attrs,
        })

    (SRC / 'pages.json').write_text(
        json.dumps(pages, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'Extracted {len(pages)} pages -> {SRC}')


if __name__ == '__main__':
    main()
