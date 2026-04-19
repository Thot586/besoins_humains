"""Ajouter une ligne de garde-fou santé mentale dans le footer de chaque page."""
import pathlib
import re

SAFETY_FR = '''    <p class="safety">Ce guide est une boussole, pas un diagnostic. Si vous traversez une période difficile, parlez-en à un professionnel. En France&nbsp;: <strong>3114</strong> (prévention du suicide, 24/7, gratuit).</p>
'''

SAFETY_EN = '''    <p class="safety">This guide is a compass, not a diagnosis. If you are going through a difficult time, reach out to a professional or a crisis line in your country.</p>
'''

# Match the author <p> line and insert the safety <p> right after it.
FR_AUTHOR = '<p class="author">Dr FENOHASINA T.J. Felicien — Psychiatre</p>\n'
EN_AUTHOR = '<p class="author">Dr FENOHASINA T.J. Felicien — Psychiatrist</p>\n'

def apply(path, author_line, safety_line):
    p = pathlib.Path(path)
    text = p.read_text(encoding='utf-8')
    if 'class="safety"' in text:
        print(f'SKIP (already has safety): {path}')
        return False
    if author_line not in text:
        print(f'MISS: {path}')
        return False
    new = text.replace(author_line, author_line + safety_line, 1)
    p.write_text(new, encoding='utf-8')
    print(f'OK:   {path}')
    return True

root = pathlib.Path('.')
ok = miss = 0

# FR: index, references, besoins/*.html
for p in [root / 'index.html', root / 'references.html']:
    if apply(p, FR_AUTHOR, SAFETY_FR): ok += 1
    else: miss += 1
for p in (root / 'besoins').glob('*.html'):
    if apply(p, FR_AUTHOR, SAFETY_FR): ok += 1
    else: miss += 1

# EN: en/index, en/references, en/needs/*.html
for p in [root / 'en' / 'index.html', root / 'en' / 'references.html']:
    if apply(p, EN_AUTHOR, SAFETY_EN): ok += 1
    else: miss += 1
for p in (root / 'en' / 'needs').glob('*.html'):
    if apply(p, EN_AUTHOR, SAFETY_EN): ok += 1
    else: miss += 1

print(f'\n{ok} applied, {miss} missed')
