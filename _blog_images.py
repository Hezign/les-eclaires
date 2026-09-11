#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute une VRAIE photo à la une (banque libre Pexels) sur chaque article de blog
et sur les cartes de l'index. Rend le blog plus humain (fini les dégradés/icônes).

    python3 _blog_images.py            # traite index + tous les articles mappés
    python3 _blog_images.py blog/mon-article.html

Idempotent : réexécutable sans dommage.
- Gabarit A (.hero)        : photo plein cadre + voile sombre, titre par-dessus.
- Gabarit B (.article-hero): la boîte à icône est remplacée par la photo.
- index.html               : vignette photo en tête de chaque carte.
- og:image + JSON-LD image : pointent vers la photo de l'article.

Les images vivent dans blog/img/ :  <slug>.jpg (bannière) + <slug>-card.jpg (vignette).
Crédit : photos Pexels (licence gratuite, usage commercial, sans attribution requise).
Pour ajouter un article : ajouter son slug + texte alt dans MAP ci-dessous, déposer
les 2 images dans blog/img/, relancer le script.
"""
import re, sys, glob, os

BASE = "https://leseclaires.fr"

# slug (= nom de fichier sans .html)  ->  texte alt (français, descriptif, honnête)
MAP = {
    "7kw-ou-22kw-quelle-puissance":
        "Recharge d'une voiture électrique sur une borne en garage : choisir la bonne puissance",
    "aides-regionales-borne-recharge-2026":
        "Couple calculant le budget d'installation d'une borne de recharge à domicile",
    "badge-rfid-itinerance-recharge-electrique-2026":
        "Automobiliste rechargeant sa voiture à une borne publique en itinérance",
    "borne-recharge-entreprise-loi-lom-2026":
        "Flotte de voitures électriques en recharge sur le parking d'une entreprise",
    "borne-recharge-nantes-installateur-aides-2026":
        "Voiture électrique en recharge dans une rue, borne de recharge à Nantes",
    "borne-recharge-poitiers-installateur-aides":
        "Électricien intervenant sur un tableau électrique, installateur de borne à Poitiers",
    "borne-recharge-solaire-autoconsommation":
        "Voiture électrique rechargée sous des panneaux solaires en autoconsommation",
    "choisir-installateur-irve-certifie":
        "Installateur IRVE certifié raccordant une borne de recharge",
    "comparatif-marques-borne-recharge-2026":
        "Borne de recharge murale affichant sa puissance, comparatif des marques",
    "cout-recharge-electrique-domicile-2026":
        "Voiture électrique en charge sur une borne murale à domicile",
    "droit-prise-copropriete":
        "Places réservées et borne de recharge dans le parking d'une copropriété",
    "entretien-duree-vie-borne-recharge-domicile":
        "Main vérifiant l'écran d'une borne de recharge lors de son entretien",
    "financement-infrastructure-collective-copropriete-advenir-2026":
        "Poignée de main scellant le financement d'une infrastructure de recharge en copropriété",
    "guide-prime-advenir-2026":
        "Signature d'un dossier d'aide pour l'installation d'une borne de recharge (prime ADVENIR)",
    "heures-creuses-recharge-voiture-electrique":
        "Bornes de recharge illuminées la nuit, recharger en heures creuses",
    "installation-borne-recharge-locataire":
        "Personne rechargeant sa voiture électrique à une borne, en tant que locataire",
    "prise-renforcee-ou-borne-de-recharge":
        "Main tenant un câble de recharge : prise renforcée ou borne ?",
    "prix-borne-de-recharge-maison-2026":
        "Femme et sa voiture électrique devant une borne de recharge à la maison",
    "recharge-bidirectionnelle-v2g-voiture-maison":
        "Voiture électrique devant une maison, recharge bidirectionnelle V2G",
    "recharge-immeuble-ancien-copropriete":
        "Voiture électrique stationnée devant un immeuble ancien en copropriété",
    "trouver-installateur-borne-recharge-pres-de-chez-soi":
        "Technicien souriant avec sa camionnette et sa caisse à outils, installateur près de chez soi",
}

COVER_CSS = """<style id="cover-css">
.hero.has-photo{position:relative;isolation:isolate;margin-top:var(--topbar-h)}
.hero.has-photo .hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.hero.has-photo .hero-scrim{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(8,16,12,.42) 0%,rgba(8,16,12,.5) 45%,rgba(8,16,12,.8) 100%)}
.hero.has-photo .hero-in{position:relative;z-index:2}
.article-hero.has-photo{height:auto;padding:0;overflow:hidden;border-radius:20px;background:#0d1a14}
.article-hero.has-photo img{display:block;width:100%;height:340px;object-fit:cover;border-radius:20px}
@media(max-width:640px){.article-hero.has-photo img{height:220px}}
</style>"""

INDEX_CSS = """<style id="cover-css-index">
.blog-card .bc-media{margin:-28px -28px 20px;border-radius:17px 17px 0 0;overflow:hidden;background:#0d1a14;aspect-ratio:16/9}
.blog-card .bc-media img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.blog-card:hover .bc-media img{transform:scale(1.04)}
@media(max-width:640px){.blog-card .bc-media{margin:-28px -28px 18px}}
</style>"""


def slug_of(path):
    return os.path.splitext(os.path.basename(path))[0]


def set_meta_image(s, url):
    """og:image + JSON-LD image -> url. Ajoute og:image si absent."""
    # og:image existant (hero.jpg / og-image.jpg / déjà /blog/img/…)
    s = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), s)
    # JSON-LD "image": "..."  (avec ou sans espace)
    s = re.sub(r'("image"\s*:\s*")https?://[^"]*?\.(?:jpg|jpeg|png|webp)(")',
               lambda m: m.group(1) + url + m.group(2), s)
    # og:image absent -> l'insérer après og:type, sinon après </title>
    if '<meta property="og:image"' not in s:
        tag = f'\n<meta property="og:image" content="{url}">'
        if '<meta property="og:type"' in s:
            s = re.sub(r'(<meta property="og:type"[^>]*>)', r'\1' + tag, s, count=1)
        else:
            s = re.sub(r'(</title>)', r'\1' + tag, s, count=1)
    return s


def inject_article(path):
    slug = slug_of(path)
    alt = MAP.get(slug)
    if not alt:
        return False  # article non mappé : on ne touche pas
    s = open(path, encoding='utf-8').read()
    o = s
    hero_img = f"/blog/img/{slug}.jpg"
    alt_esc = alt.replace('"', '&quot;')

    # CSS (remplace le bloc existant pour propager les corrections, sinon insère)
    if 'id="cover-css"' in s:
        s = re.sub(r'<style id="cover-css">.*?</style>', lambda m: COVER_CSS, s, count=1, flags=re.DOTALL)
    elif '</head>' in s:
        s = s.replace('</head>', COVER_CSS + '\n</head>', 1)

    # Gabarit A : .hero -> photo plein cadre + voile
    if 'class="hero-bg"' not in s:
        img = (f'<img class="hero-bg" src="{hero_img}" alt="{alt_esc}" '
               f'loading="eager" fetchpriority="high" width="1400" height="620">'
               f'<span class="hero-scrim"></span>')
        s = s.replace('<div class="hero"><div class="hero-in">',
                      f'<div class="hero has-photo">{img}<div class="hero-in">', 1)

    # Gabarit B : .article-hero (boîte icône) -> photo
    if 'article-hero' in s and 'article-hero has-photo' not in s:
        img = (f'<div class="article-hero has-photo"><img src="{hero_img}" '
               f'alt="{alt_esc}" loading="lazy" width="1200" height="480"></div>')
        s = re.sub(r'<div class="article-hero"[^>]*>.*?</div>', img, s,
                   count=1, flags=re.DOTALL)

    # Rafraîchit l'alt si la photo (donc le texte) a changé depuis une injection précédente
    s = re.sub(r'(<img class="hero-bg" src="' + re.escape(hero_img) + r'" alt=")[^"]*(")',
               lambda m: m.group(1) + alt_esc + m.group(2), s)
    s = re.sub(r'(<div class="article-hero has-photo"><img src="' + re.escape(hero_img) + r'" alt=")[^"]*(")',
               lambda m: m.group(1) + alt_esc + m.group(2), s)

    # Métadonnées image
    s = set_meta_image(s, f"{BASE}{hero_img}")

    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def inject_index(path='blog/index.html'):
    s = open(path, encoding='utf-8').read()
    o = s
    if 'id="cover-css-index"' in s:
        s = re.sub(r'<style id="cover-css-index">.*?</style>', lambda m: INDEX_CSS, s, count=1, flags=re.DOTALL)
    elif '</head>' in s:
        s = s.replace('</head>', INDEX_CSS + '\n</head>', 1)

    # injecte la vignette juste après l'ouverture de carte, si pas déjà présente.
    # le groupe 2 capture un éventuel <div class="bc-media"> déjà là -> idempotent.
    def repl(m):
        head, slug, existing = m.group(1), m.group(2), m.group(3)
        if existing:                       # déjà injecté
            return m.group(0)
        alt = MAP.get(slug)
        if not alt:
            return m.group(0)
        media = (f'\n          <div class="bc-media"><img src="/blog/img/{slug}-card.jpg" '
                 f'alt="{alt.replace(chr(34), "&quot;")}" loading="lazy" '
                 f'width="640" height="420"></div>')
        return head + media

    s = re.sub(
        r'(<a class="blog-card" href="/blog/([a-z0-9\-]+)\.html">)(\s*<div class="bc-media">)?',
        repl, s)

    # Rafraîchit l'alt des vignettes déjà présentes si le texte a changé
    def refresh_alt(m):
        slug = m.group(1)
        alt = MAP.get(slug)
        if not alt:
            return m.group(0)
        return (f'<div class="bc-media"><img src="/blog/img/{slug}-card.jpg" alt="'
                + alt.replace(chr(34), "&quot;") + '"')
    s = re.sub(r'<div class="bc-media"><img src="/blog/img/([a-z0-9\-]+)-card\.jpg" alt="[^"]*"',
               refresh_alt, s)

    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


# ── HOME : cartes blog des 3 derniers articles (auto) ──────────────────────
FR_MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
           'août', 'septembre', 'octobre', 'novembre', 'décembre']

HOME_BLOG_CSS = """<style id="home-blog-css">
.blog-grid .blog-thumb{background:#0d1a14}
.blog-grid .blog-thumb::after{display:none}
.blog-grid .blog-thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}
.blog-grid .blog-tag{background:rgba(255,255,255,.92);color:#0d1a14;border:none;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
</style>"""


def _find(s, pattern):
    m = re.search(pattern, s, re.I | re.S)
    return m.group(1).strip() if m else ''


def article_info(slug):
    path = f'blog/{slug}.html'
    if not os.path.exists(path):
        return None
    s = open(path, encoding='utf-8').read()
    date = _find(s, r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})')
    title = _find(s, r'<title>(.*?)</title>')
    title = re.sub(r'\s*[|·\-–—]?\s*Les [ÉEée]clair[ée]s\s*$', '', title).strip()
    desc = (_find(s, r'<meta name="description" content="([^"]*)"')
            or _find(s, r'<meta property="og:description" content="([^"]*)"'))
    badge = _find(s, r'<div class="badge">([^<]*)</div>')
    return {'slug': slug, 'date': date, 'title': title, 'desc': desc, 'badge': badge}


def update_home(path='index.html'):
    if not os.path.exists(path):
        return False
    s = open(path, encoding='utf-8').read()
    o = s

    # 3 articles les plus récents parmi ceux qui ont une photo (dans MAP)
    infos = [i for i in (article_info(sl) for sl in MAP) if i and i['date']]
    infos.sort(key=lambda i: i['date'], reverse=True)
    top = infos[:3]
    if len(top) < 3:
        return False

    # CSS (remplace ou insère)
    if 'id="home-blog-css"' in s:
        s = re.sub(r'<style id="home-blog-css">.*?</style>', lambda m: HOME_BLOG_CSS, s, count=1, flags=re.S)
    elif '</head>' in s:
        s = s.replace('</head>', HOME_BLOG_CSS + '\n</head>', 1)

    def esc(t):
        return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    cards = []
    for i, info in enumerate(top, start=1):
        slug = info['slug']
        alt = MAP[slug].replace('"', '&quot;')
        y, m, _d = info['date'].split('-')
        datefr = f"{FR_MOIS[int(m)].capitalize()} {y}"
        cards.append(
            f'<a href="blog/{slug}.html" class="blog-card reveal rd{i}">\n'
            f'        <div class="blog-thumb"><img src="/blog/img/{slug}-card.jpg" '
            f'alt="{alt}" loading="lazy" width="640" height="420"><span class="blog-tag">{esc(info["badge"])}</span></div>\n'
            f'        <div class="blog-body">\n'
            f'          <div class="blog-date">{datefr}</div>\n'
            f'          <div class="blog-title">{esc(info["title"])}</div>\n'
            f'          <div class="blog-excerpt">{esc(info["desc"])}</div>\n'
            f'          <span class="blog-cta">Lire l\'article →</span>\n'
            f'        </div>\n'
            f'      </a>')
    grid = '<div class="blog-grid">\n      ' + '\n      '.join(cards) + '\n    </div>'

    s = re.sub(r'<div class="blog-grid">\s*(?:<a [^>]*class="blog-card[^"]*"[^>]*>.*?</a>\s*)+</div>',
               lambda m: grid, s, count=1, flags=re.S)

    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        for f in args:
            if f.rstrip('/').endswith('blog/index.html'):
                ok = inject_index(f)
            elif os.path.basename(f) == 'index.html':
                ok = update_home(f)
            else:
                ok = inject_article(f)
            print(('maj  ' if ok else 'skip ') + f)
    else:
        n = 0
        if inject_index():
            print('maj  blog/index.html'); n += 1
        if update_home('index.html'):
            print('maj  index.html (home)'); n += 1
        for f in sorted(glob.glob('blog/*.html')):
            if f.endswith(('index.html', 'template.html')):
                continue
            if inject_article(f):
                print('maj  ' + f); n += 1
        print(f"--- {n} fichier(s) mis à jour ---")
