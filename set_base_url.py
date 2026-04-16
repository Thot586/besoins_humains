"""
Reconfigure the production domain across all files.

Usage: python set_base_url.py https://votre-domaine.fr
       python set_base_url.py --reset     (back to https://example.com)
"""
import os, sys, re

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(content.replace(old, new))
        return True
    return False

def current_base_url():
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        match = re.search(r'<loc>(https?://[^/<]+)', f.read())
    return match.group(1) if match else None

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]
    new_base = 'https://example.com' if arg == '--reset' else arg.rstrip('/')
    if not new_base.startswith(('http://', 'https://')):
        print(f"Invalid URL: {new_base!r} (must start with http:// or https://)")
        sys.exit(1)

    old_base = current_base_url()
    if not old_base:
        print("Could not detect current base URL in sitemap.xml")
        sys.exit(1)
    if old_base == new_base:
        print(f"Base URL already set to {new_base}")
        return

    targets = ['sitemap.xml', 'robots.txt']
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                targets.append(os.path.join(root, f))

    updated = 0
    for path in targets:
        if replace_in_file(path, old_base, new_base):
            updated += 1

    print(f"Base URL: {old_base}  ->  {new_base}")
    print(f"Files updated: {updated}")

if __name__ == '__main__':
    main()
