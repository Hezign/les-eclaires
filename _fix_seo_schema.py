#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2 - Ajoute un BlogPosting aux articles qui n'en ont pas.
P6 - Ajoute un BreadcrumbList (Accueil > Blog > article) aux articles qui n'en ont pas.
Format aligné sur les articles générés par n8n. Idempotent (n'ajoute que si absent).
Insertion juste avant </head>.
"""
import pathlib, re, json

BLOG = pathlib.Path(__file__).parent / "blog"
BASE = "https://leseclaires.fr"

# Dates de secours pour les articles sans article:published_time ni datePublished
DATE_FALLBACK = {
    "7kw-ou-22kw-quelle-puissance": "2026-01-15",
    "guide-prime-advenir-2026":     "2025-12-31",
}

def get(pattern, txt, default=None):
    m = re.search(pattern, txt)
    return m.group(1) if m else default

changed = []
for f in sorted(BLOG.glob("*.html")):
    if f.name in ("index.html", "template.html"):
        continue
    stem = f.stem
    txt = f.read_text(encoding="utf-8")
    orig = txt
    url = f"{BASE}/blog/{f.name}"

    title = get(r"<title>(.*?)</title>", txt, "")
    desc  = get(r'<meta name="description" content="([^"]*)"', txt, "")
    image = get(r'<meta property="og:image" content="([^"]*)"', txt, f"{BASE}/blog/img/{stem}.jpg")
    date  = get(r'article:published_time" content="(\d{4}-\d{2}-\d{2})', txt) \
            or get(r'"datePublished":"(\d{4}-\d{2}-\d{2})', txt) \
            or DATE_FALLBACK.get(stem)
    datemod = get(r'article:modified_time" content="(\d{4}-\d{2}-\d{2})', txt) \
              or get(r'"dateModified":"(\d{4}-\d{2}-\d{2})', txt) \
              or date

    inserts = []

    # P2 : BlogPosting si absent
    if '"@type":"BlogPosting"' not in txt:
        if not date:
            print(f"!! {f.name} : pas de date, BlogPosting ignoré")
        else:
            bp = {
                "@context": "https://schema.org", "@type": "BlogPosting",
                "headline": title, "description": desc, "image": image, "url": url,
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "datePublished": date, "dateModified": datemod,
                "author": {"@type": "Organization", "name": "Les Éclairés", "url": f"{BASE}/"},
                "publisher": {"@type": "Organization", "name": "Les Éclairés",
                              "logo": {"@type": "ImageObject", "url": f"{BASE}/favicon.png"}},
            }
            inserts.append(json.dumps(bp, ensure_ascii=False, separators=(",", ":")))

    # P6 : BreadcrumbList si absent
    if "BreadcrumbList" not in txt:
        bc = {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": url},
            ],
        }
        inserts.append(json.dumps(bc, ensure_ascii=False, separators=(",", ":")))

    if inserts:
        block = "".join(f'<script type="application/ld+json">{j}</script>\n' for j in inserts)
        txt = txt.replace("</head>", block + "</head>", 1)

    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        tag = []
        if '"@type":"BlogPosting"' in "".join(inserts): tag.append("BlogPosting")
        if "BreadcrumbList" in "".join(inserts): tag.append("BreadcrumbList")
        changed.append((f.name, "+".join(tag)))

print(f"=== {len(changed)} FICHIERS MODIFIÉS ===")
for name, tags in changed:
    print(f"  + {tags:28s} {name}")
