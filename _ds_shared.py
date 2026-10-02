#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Composants partagés (design system) pour toutes les pages SAUF l'accueil,
qui reste la référence : bouton principal, petit titre de section (kicker ⚡),
FAQ (cartes + chevron), espace sous le header, interlignes des titres.

Injecte <style id="ds-shared"> en fin de <head> (gagne sur le CSS de la page à
spécificité égale). Idempotent. Appelé par _apply_dark.apply() (donc par les
générateurs villes/copro/simulateur et _normalize_blog) ; exécutable en direct :

    python3 _ds_shared.py
"""
import glob
import os
import re

BOLT = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E"
        "%3Cpath d='M13 2L4 13.5h6.2L9 22l9-12.5h-6.2L13 2z'/%3E%3C/svg%3E\") center/contain no-repeat")
CHEVRON = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
           "stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E"
           "%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E\") center/contain no-repeat")

CSS = f'''<style id="ds-shared">
/* Bouton principal unique (référence : .btn-primary de l'accueil) */
.btn-primary,.btn-vert,.btn-submit,.nf-btn.primary,.pt-btn-main{{background:var(--c-vert-lt);color:#0a0a09;font-family:var(--ff-h);font-weight:700;letter-spacing:-.02em;border:none}}
.btn-primary:hover,.btn-vert:hover,.btn-submit:hover,.nf-btn.primary:hover,.pt-btn-main:hover{{background:var(--c-vert);color:#0a0a09;box-shadow:0 10px 28px rgba(0,194,126,.32)}}
.btn-submit:disabled{{background:var(--c-vert-lt);opacity:.5}}
/* Petit titre de section unique : ⚡ + capitales vertes */
.section-tag,.page-tag,.pt-kicker{{display:flex;align-items:center;gap:8px;font-family:var(--ff-b);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.12em;color:var(--c-vert-txt);margin-bottom:16px}}
.section-tag,.pt-kicker{{display:inline-flex}}
.pt-kicker::before{{content:'';display:inline-block;width:12px;height:12px;flex-shrink:0;background:var(--c-vert);-webkit-mask:{BOLT};mask:{BOLT}}}
.pt-sec.band .pt-kicker{{color:var(--c-vert-lt)}}
/* FAQ unique : cartes blanches + chevron (comme l'accueil) */
.faq-city details,.pt-faq details{{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:16px;margin-bottom:12px;transition:border-color .2s}}
.pt-faq{{gap:0}}
.faq-city details[open],.pt-faq details[open]{{border-color:var(--c-vert-br)}}
.faq-city summary,.pt-faq summary{{padding:20px 24px;font-family:var(--ff-h);font-size:16px;font-weight:700;letter-spacing:-.025em;color:var(--c-ink);align-items:center}}
.faq-city summary:hover,.pt-faq summary:hover{{color:var(--c-vert-txt)}}
.faq-city summary::after,.pt-faq summary::after,.faq-city details[open] summary::after,.pt-faq details[open] summary::after{{content:'';width:20px;height:20px;flex-shrink:0;background:var(--c-muted);-webkit-mask:{CHEVRON};mask:{CHEVRON};transition:transform .25s}}
.faq-city details[open] summary::after,.pt-faq details[open] summary::after{{transform:rotate(180deg);background:var(--c-vert)}}
.faq-city details>div,.pt-faq details p{{padding:0 24px 20px;font-size:15px;line-height:1.8;color:var(--c-mid)}}
.faq-city details>div a{{color:var(--c-vert-txt)}}
/* Espace commun entre le header et le début du contenu */
.hero-city,.page,.nf-wrap,.blog-wrap,.pt-hero{{padding-top:calc(var(--topbar-h,40px) + 120px)}}
.simp-hero{{padding-top:calc(var(--topbar-h,40px) + 100px)}}
@media(max-width:640px){{.hero-city,.page,.simp-hero,.nf-wrap,.blog-wrap,.pt-hero{{padding-top:calc(var(--topbar-h,40px) + 100px)!important}}}}
/* Interlignes des titres (hérités du texte = 1,6 : trop lâches) */
.hero-city h1,.page h1,.page-title,.city-body h2,.blog-head h1,.nf-wrap h1{{line-height:1.08}}
.city-body h2{{line-height:1.15}}
@media(max-width:640px){{.hero-city h1 br{{display:none}}}}
</style>'''

SKIP = ('index.html', 'template.html')


def eligible(path):
    b = os.path.basename(path)
    if path == 'index.html' or b.endswith('-preview.html'):
        return False
    if b.startswith(('email-', 'signature-mail')):
        return False
    return True


def apply(path):
    if not eligible(path):
        return False
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    o = s
    s = re.sub(r'<style id="ds-shared">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


if __name__ == '__main__':
    files = [f for f in glob.glob('*.html') + glob.glob('villes/*.html') + glob.glob('blog/*.html')]
    n = sum(apply(f) for f in files)
    print(f'{n} page(s) mises à jour')
