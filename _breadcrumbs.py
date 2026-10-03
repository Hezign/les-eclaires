#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fil d'Ariane visible sur les pages qui n'en avaient pas : articles, accueil du blog,
simulateur, pages légales. (Copropriété, entreprise, partenaires et villes le reçoivent
de hs.hero ; leur style est repris ici.) Idempotent : le bloc est balisé <!--bc-->…<!--/bc-->.

    python3 _breadcrumbs.py     # toutes les pages concernées
"""
import glob
import html
import json
import re

CSS = '''<style id="bc-css">
.breadcrumb.bc{font-size:13px;line-height:1.5;color:var(--c-muted);margin:0 0 18px;display:flex;flex-wrap:wrap;gap:0 6px;min-width:0}
.breadcrumb.bc a{color:inherit;text-decoration:none}
.breadcrumb.bc a:hover{color:var(--c-vert-txt,#007A50);text-decoration:underline}
.breadcrumb.bc span[aria-current]{color:var(--c-text,var(--c-ink));max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hero .breadcrumb.bc{color:rgba(255,255,255,.72);margin-bottom:20px}
.hero .breadcrumb.bc a:hover{color:#fff}
.hero .breadcrumb.bc span[aria-current]{color:#fff}
</style>'''

LEGAL = {'mentions-legales.html': 'Mentions légales', 'confidentialite.html': 'Confidentialité',
         'cgu.html': "Conditions d'utilisation"}


def block(trail):
    """trail = [(libellé, href|None)] ; le dernier élément est la page courante."""
    parts = []
    for label, href in trail[:-1]:
        parts.append(f'<a href="{href}">{label}</a><span aria-hidden="true">›</span>')
    parts.append(f'<span aria-current="page">{trail[-1][0]}</span>')
    return ('<!--bc--><div class="breadcrumb bc" role="navigation" aria-label="Fil d\'Ariane">'
            + ''.join(parts) + '</div><!--/bc-->')


def ld(trail, url):
    items = []
    base = 'https://leseclaires.fr'
    for i, (label, href) in enumerate(trail, 1):
        items.append({"@type": "ListItem", "position": i, "name": html.unescape(label),
                      "item": base + (href if href else url)})
    return ('<script type="application/ld+json" id="bc-ld">'
            + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items},
                         ensure_ascii=False) + '</script>')


def plan(path, s):
    """Retourne (trail, motif d'ancrage, position 'after'|'before', ajouter_ld)."""
    if path == 'blog/index.html':
        return [('Accueil', '/'), ('Guides', None)], r'<div class="blog-head">\s*', 'after', False
    if path.startswith('blog/'):
        m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else 'Article'
        return [('Accueil', '/'), ('Guides', '/blog/'), (title, None)], r'<div class="hero-in">\s*', 'after', False
    if path == 'simulateur.html':
        return [('Accueil', '/'), ('Simulateur', None)], r'<div class="simp-badge">', 'before', False
    if path in LEGAL:
        return [('Accueil', '/'), (LEGAL[path], None)], r'<div class="page-tag">', 'before', True
    return None


def apply(path):
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    p = plan(path, s)
    if not p:
        return False
    trail, anchor, pos, add_ld = p
    o = s
    s = re.sub(r'<!--bc-->.*?<!--/bc-->\s*', '', s, flags=re.S)
    m = re.search(anchor, s)
    if not m:
        return False
    at = m.end() if pos == 'after' else m.start()
    s = s[:at] + block(trail) + '\n' + s[at:]
    s = re.sub(r'<style id="bc-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = re.sub(r'<script type="application/ld\+json" id="bc-ld">.*?</script>\n?', '', s, flags=re.S)
    if add_ld:
        url = '/' + path
        s = s.replace('</head>', ld(trail, url) + '\n</head>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def targets():
    return (['simulateur.html', 'blog/index.html'] + list(LEGAL)
            + [f for f in sorted(glob.glob('blog/*.html')) if not f.endswith('index.html')])


if __name__ == '__main__':
    n = sum(apply(f) for f in targets())
    print(f'{n} fil(s) d\'Ariane posés ou mis à jour')
