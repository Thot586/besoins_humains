"""Remplacer le bloc pseudo-satisfacteur (v2 spécifique, redondant avec les items)
par une formulation méta, dépouillée, qui pointe vers la liste au lieu de la dupliquer."""
import pathlib
import re

# Suffixes de rattachement au besoin
FR_SUFFIX = {
    'affection': "à l'affection",
    'comprehension': "à la compréhension",
    'creation': "à la création",
    'identite': "à l'identité",
    'liberte': "à la liberté",
    'loisir': "au loisir",
    'participation': "à la participation",
    'protection': "à la protection",
    'subsistance': "à la subsistance",
}
EN_SUFFIX = {
    'affection': "to affection",
    'understanding': "to understanding",
    'creation': "to creation",
    'identity': "to identity",
    'freedom': "to freedom",
    'leisure': "to leisure",
    'participation': "to participation",
    'protection': "to protection",
    'subsistence': "to subsistence",
}

def fr_block(need_suffix):
    return f"Max-Neef nomme <strong>pseudo-satisfacteur</strong> ce qui prend la place d'une réponse au besoin sans en remplir le rôle. Les faux amis ci-dessous en sont les formes propres {need_suffix}."

def en_block(need_suffix):
    return f"Max-Neef names a <strong>pseudo-satisfier</strong> anything that takes the place of a response to the need without filling the role. The pitfalls below are the forms specific {need_suffix}."

# Pattern to match the current <p> content inside the concept-note-body
# We target the FIRST <p>…</p> inside the concept-note-body (which is the only one).
FR_PATTERN = re.compile(
    r'(<details class="concept-note">\s*<summary>[^<]*</summary>\s*<div class="concept-note-body">\s*<p>)(.*?)(</p>\s*</div>\s*</details>)',
    re.DOTALL
)
EN_PATTERN = FR_PATTERN  # same structure

def apply(path, new_content, pattern=FR_PATTERN):
    p = pathlib.Path(path)
    t = p.read_text(encoding='utf-8')
    new_text, n = pattern.subn(lambda m: m.group(1) + new_content + m.group(3), t, count=1)
    if n == 0:
        print(f'MISS: {path}')
        return False
    p.write_text(new_text, encoding='utf-8')
    print(f'OK:   {path}')
    return True

ok = miss = 0
for slug, suffix in FR_SUFFIX.items():
    if apply(f'besoins/{slug}.html', fr_block(suffix)):
        ok += 1
    else:
        miss += 1

for slug, suffix in EN_SUFFIX.items():
    if apply(f'en/needs/{slug}.html', en_block(suffix)):
        ok += 1
    else:
        miss += 1

print(f'\n{ok} applied, {miss} missed')
