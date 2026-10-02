#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Index du blog + catégories normalisées. Idempotent.

- 6 catégories au lieu de 17 libellés n8n disparates : appliquées à la carte de
  l'index (.bc-tag + data-cat) ET au badge de l'article (.badge), donc aussi aux
  cartes de l'accueil (update_home lit le badge de l'article).
- Dates complètes depuis datePublished (« 1er octobre 2026 »).
- En-tête aligné à gauche avec kicker ⚡, conteneur 984 px, filtres par catégorie.

À relancer après chaque publication n8n (branché dans _normalize_blog.py).
    python3 _blog_index.py
"""
import glob
import re

CATS = ['Choisir & installer', 'Aides & prix', 'Copropriété', 'Entreprise',
        'Recharge au quotidien', 'Espace pro']

BY_SLUG = {
    'aides-regionales-borne-recharge-2026': 'Aides & prix',
    'prix-borne-de-recharge-maison-2026': 'Aides & prix',
    'cout-recharge-electrique-domicile-2026': 'Aides & prix',
    'guide-prime-advenir-2026': 'Aides & prix',
    'zaptec-ou-hager-borne-copropriete': 'Copropriété',
    'financement-infrastructure-collective-copropriete-advenir-2026': 'Copropriété',
    'recharge-immeuble-ancien-copropriete': 'Copropriété',
    'droit-prise-copropriete': 'Copropriété',
    'heures-creuses-recharge-voiture-electrique': 'Recharge au quotidien',
    'borne-recharge-solaire-autoconsommation': 'Recharge au quotidien',
    'badge-rfid-itinerance-recharge-electrique-2026': 'Recharge au quotidien',
    'recharge-bidirectionnelle-v2g-voiture-maison': 'Recharge au quotidien',
    'borne-recharge-entreprise-loi-lom-2026': 'Entreprise',
    'logiciel-gestion-installateur-irve': 'Espace pro',
    'devenir-installateur-agree-advenir': 'Espace pro',
}

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']


def guess(raw, slug):
    """Catégorie d'un nouvel article (n8n) d'après son libellé brut et son slug."""
    t = (raw + ' ' + slug).lower()
    if 'installateur-irve' in slug or 'espace pro' in t or 'installateur agr' in t:
        return 'Espace pro'
    if 'copro' in t or 'syndic' in t or 'immeuble' in t:
        return 'Copropriété'
    if 'entreprise' in t or 'flotte' in t or 'lom' in t:
        return 'Entreprise'
    if re.search(r'aide|prix|co[uû]t|subvention|advenir|tarif', t):
        return 'Aides & prix'
    if re.search(r'heures-creuses|itin|solaire|v2g|mobilit', t):
        return 'Recharge au quotidien'
    return 'Choisir & installer'


def cat_of(slug, raw=''):
    return BY_SLUG.get(slug) or guess(raw, slug)


def fr_date(iso):
    y, m, d = int(iso[:4]), int(iso[5:7]), int(iso[8:10])
    return f"{'1er' if d == 1 else d} {MOIS[m - 1]} {y}"


def data_slug(cat):
    return re.sub(r'[^a-z]+', '-', cat.lower().replace('é', 'e').replace('&', '')).strip('-')


CSS = '''<style id="blog-index-css">
.blog-wrap{max-width:1032px;width:100%;box-sizing:border-box}
.blog-head{text-align:left;max-width:720px;margin:0 0 36px}
.blog-head h1{font-size:clamp(34px,5vw,56px);letter-spacing:-.045em}
.blog-filters{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 36px}
.blog-filters button{font:inherit;font-family:var(--ff-h);font-size:14px;font-weight:700;letter-spacing:-.01em;padding:9px 16px;border-radius:999px;border:1px solid var(--c-border2);background:var(--c-bg2);color:var(--c-ink);cursor:pointer;transition:border-color .2s,background .2s}
.blog-filters button:hover{border-color:var(--c-vert-br)}
.blog-filters button[aria-pressed="true"]{background:var(--c-band);border-color:var(--c-band);color:#fff}
html[data-theme="dark"] .blog-filters button[aria-pressed="true"]{background:var(--c-vert-lt);border-color:var(--c-vert-lt);color:#05231a}
.blog-filters .n{opacity:.55;font-weight:500;margin-left:6px}
.bc-tag{color:var(--c-vert-txt)}
.bc-more{color:var(--c-vert-txt)}
.blog-card[hidden]{display:none}
@media(max-width:640px){.blog-filters{flex-wrap:nowrap;overflow-x:auto;margin:0 -24px 28px;padding:0 24px 4px;scrollbar-width:none}.blog-filters::-webkit-scrollbar{display:none}.blog-filters button{flex:none}}
</style>'''

JS = '''<script id="blog-index-js">(function(){var f=document.querySelector('.blog-filters');if(!f)return;
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var c=b.getAttribute('data-cat');
f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
document.querySelectorAll('.blog-card').forEach(function(a){a.hidden=!!c&&a.getAttribute('data-cat')!==c;});});})();</script>'''


def build(path='blog/index.html'):
    s = open(path, encoding='utf-8').read()
    o = s
    counts = {}

    def card(m):
        head, slug, mid, raw, date_html = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        cat = cat_of(slug, raw)
        counts[cat] = counts.get(cat, 0) + 1
        try:
            a = open(f'blog/{slug}.html', encoding='utf-8').read()
            dp = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', a)
            date_txt = fr_date(dp.group(1)) if dp else date_html
        except FileNotFoundError:
            date_txt = date_html
        head = re.sub(r'\s*data-cat="[^"]*"', '', head)
        head = head.replace('class="blog-card"', f'class="blog-card" data-cat="{data_slug(cat)}"', 1)
        return f'{head}{mid}<span class="bc-tag">{cat}</span>\n          <span class="bc-date">{date_txt}</span>'

    s = re.sub(r'(<a class="blog-card"[^>]*href="/blog/([a-z0-9\-]+)\.html"[^>]*>)(.*?)'
               r'<span class="bc-tag">([^<]*)</span>\s*<span class="bc-date">([^<]*)</span>',
               card, s, flags=re.S)
    s = s.replace("Lire l article →", "Lire l'article →")

    # En-tête : kicker + filtres
    s = re.sub(r'\s*<span class="section-tag">Le blog</span>', '', s)
    s = s.replace('<div class="blog-head">', '<div class="blog-head">\n      <span class="section-tag">Le blog</span>', 1)
    total = sum(counts.values())
    btns = (f'<button type="button" aria-pressed="true" data-cat="">Tous<span class="n">{total}</span></button>'
            + ''.join(f'<button type="button" aria-pressed="false" data-cat="{data_slug(c)}">{c}<span class="n">{counts[c]}</span></button>'
                      for c in CATS if counts.get(c)))
    s = re.sub(r'\s*<div class="blog-filters"[^>]*>.*?</div>', '', s, flags=re.S)
    s = s.replace('<div class="blog-grid">', f'<div class="blog-filters" role="group" aria-label="Filtrer par catégorie">{btns}</div>\n    <div class="blog-grid">', 1)

    s = re.sub(r'<style id="blog-index-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = re.sub(r'<script id="blog-index-js">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</body>', JS + '\n</body>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
    return counts


def badges():
    """Badge du hero de chaque article = catégorie normalisée."""
    n = 0
    for f in glob.glob('blog/*.html'):
        if f.endswith(('index.html', 'template.html')):
            continue
        slug = f[5:-5]
        s = open(f, encoding='utf-8').read()
        m = re.search(r'<div class="badge">([^<]*)</div>', s)
        if not m:
            continue
        cat = cat_of(slug, m.group(1))
        if m.group(1) != cat:
            s = s.replace(m.group(0), f'<div class="badge">{cat}</div>', 1)
            open(f, 'w', encoding='utf-8').write(s)
            n += 1
    return n


if __name__ == '__main__':
    b = badges()
    c = build()
    print(f'{b} badge(s) d\'article normalisé(s) ; index : {c}')
