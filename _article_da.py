#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remet les articles du gabarit `.hero` (articles n8n + blog/template.html) sur la DA.

Ce gabarit a ses couleurs en dur et ne définit pas les tokens de base du site
(--ff-h, --c-vert, --c-ink...) : police Inter non chargée, bouton « Accepter »
des cookies invisible (fond var(--c-vert) indéfini en clair), mode sombre
illisible (texte gris/noir sur fond noir).

Injecte un bloc <style id="article-da"> en fin de <head> (après le CSS de
l'article et theme-tokens) : tokens clairs par défaut + surcharges en tokens.
Le sombre reste piloté par html[data-theme="dark"] (_apply_dark.py), plus
spécifique que :root. Idempotent.

    python3 _article_da.py              # tous les articles .hero + template
    python3 _article_da.py blog/x.html  # un article
Appelé aussi par _normalize_blog.py (à chaque publication n8n).
"""
import glob
import re
import sys

CSS = '''<style id="article-da">
:root{--ff-h:'Schibsted Grotesk',sans-serif;--ff-b:'Manrope',sans-serif;--c-bg:#F4F6F5;--c-bg2:#FFFFFF;--c-ink:#000000;--c-text:#1A1D1B;--c-mid:#454B48;--c-muted:#5C6560;--c-border:rgba(0,0,0,.08);--c-border2:rgba(0,0,0,.13);--c-vert:#00C27E;--c-vert-lt:#00F5A0;--c-vert-bg:rgba(0,194,126,.08);--c-vert-br:rgba(0,194,126,.22)}
body{font-family:var(--ff-b);background:var(--c-bg);color:var(--c-text)}
.toc{background:var(--c-bg2);border-color:var(--c-border)}
.toc h3{color:var(--c-vert-txt)}
.toc a{color:var(--c-mid)}
.toc a:hover,.toc a.on{color:var(--c-vert-txt);border-left-color:var(--c-vert)}
.scta,.ctafin,.prose .ctamid{background:var(--c-band)}
.prose p,.prose ul li,.prose ol li{color:var(--c-mid);font-weight:400}
.prose strong,.prose h2,.prose h3{color:var(--c-ink)}
.prose .ctamid h3{color:#fff}
.prose ul li{border-bottom-color:var(--c-border)}
.prose a{color:var(--c-vert-txt);text-decoration-color:var(--c-vert-br)}
.prose a:hover{text-decoration-color:var(--c-vert-txt)}
.prose table{border-color:var(--c-border)}
.prose th{background:var(--c-band)}
.prose td{color:var(--c-mid);border-bottom-color:var(--c-border)}
.prose blockquote{background:var(--c-bg2);color:var(--c-mid)}
.scta a,.prose .ctamid a,.bg{background:var(--c-vert-lt);color:#000}
.scta a.s{background:rgba(255,255,255,.08);color:#fff}
footer{background:var(--c-bg);border-top-color:var(--c-border)}
footer .footer-top{border-bottom-color:var(--c-border)}
footer .footer-col h4,footer .footer-cities h4{color:var(--c-muted)}
footer .footer-col li a,footer .footer-cities-list a{color:var(--c-mid)}
footer .footer-col li a:hover,footer .footer-cities-list a:hover{color:var(--c-vert-txt)}
footer .footer-bottom .f-brand-name{color:#08130d}
/* Lot 2 : un seul axe de 984 px (comme le header/footer) pour le hero et le corps */
.hero-in{max-width:984px}
.htitle{max-width:860px}
.layout{max-width:1032px}
/* Tableaux pleine largeur, défilement horizontal dans un conteneur sur mobile */
.prose .table-wrap{overflow-x:auto;margin:28px 0;border:1px solid var(--c-border);border-radius:12px;background:var(--c-bg2)}
.prose .table-wrap table{display:table;width:100%;margin:0;border:none;border-radius:0;overflow:visible}
.prose .table-wrap td{background:transparent}
html[data-theme="dark"] .scta,html[data-theme="dark"] .ctafin,html[data-theme="dark"] .prose .ctamid{border:1px solid var(--c-border2)}
</style>'''


def is_hero_article(s):
    return 'class="hero' in s and 'class="prose' in s


def apply(path):
    s = open(path, encoding='utf-8').read()
    if not is_hero_article(s):
        return False
    o = s
    s = re.sub(r'<style id="article-da">.*?</style>\n?', '', s, flags=re.S)
    # Tableaux enveloppés une seule fois dans .table-wrap
    s = re.sub(r'(?<!<div class="table-wrap">)(<table\b.*?</table>)',
               r'<div class="table-wrap">\1</div>', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


if __name__ == '__main__':
    files = sys.argv[1:] or [f for f in sorted(glob.glob('blog/*.html')) if not f.endswith('index.html')]
    n = sum(apply(f) for f in files)
    print(f'{n} article(s) mis à jour')
