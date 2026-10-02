#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Règles légales et de marque appliquées à TOUTES les pages (accueil compris).
Idempotent. Appelé par _apply_dark.apply() ; exécutable en direct :

    python3 _legal_global.py

1. Google Analytics chargé UNIQUEMENT après acceptation des cookies (plus de
   script Google ni de signal sans cookie avant le choix). Cookies _ga limités à
   13 mois (recommandation CNIL ; défaut Google = 2 ans).
2. Lien « Conditions d'utilisation » (/cgu.html) dans le footer, après Confidentialité.
3. Aucune icône dollar : remplacée par l'icône euro.
"""
import glob
import os
import re

GA_ID = 'G-ZXGFCVHHDM'
DENIED = "{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'}"
GRANTED = "{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'}"

GA_BLOCK = (
    '<!-- Google Analytics : chargé seulement après consentement (_legal_global.py) -->\n'
    '<script id="ga-consent">\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    '  function gtag(){dataLayer.push(arguments);}\n'
    f"  gtag('consent','default',{DENIED});\n"
    '  window.leLoadGA=function(){if(window.__leGA)return;window.__leGA=1;'
    f"gtag('consent','update',{GRANTED});"
    "var s=document.createElement('script');s.async=true;"
    f"s.src='https://www.googletagmanager.com/gtag/js?id={GA_ID}';document.head.appendChild(s);"
    f"gtag('js',new Date());gtag('config','{GA_ID}',{{cookie_expires:33696000}});}};\n"
    "  try{if(localStorage.getItem('les-eclaires-cookie-v2')==='y')window.leLoadGA();}catch(e){}\n"
    '</script>'
)

OLD_GA = re.compile(
    r'(?:<!-- Google tag \(gtag\.js\) -->\s*)?'
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=' + GA_ID + r'"></script>\s*'
    r'<script>\s*window\.dataLayer.*?gtag\(\'config\', ?\'' + GA_ID + r'\'\);(.*?)</script>', re.S)

ACCEPT_OLD = "try{if(window.gtag)gtag('consent','update',"
ACCEPT_NEW = "try{if(ok&&window.leLoadGA)window.leLoadGA();if(window.gtag)gtag('consent','update',"

DOLLAR = '<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'
EURO = '<path d="M18 7a7 7 0 1 0 0 10M4 10h10M4 14h10"/>'

CGU_LI = '<li><a href="/cgu.html">Conditions d\'utilisation</a></li>'


def apply(path):
    b = os.path.basename(path)
    if b.startswith(('email-', 'signature-mail')):
        return False
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    o = s
    # 1. GA après consentement
    if 'id="ga-consent"' in s:
        s = re.sub(r'<!-- Google Analytics : chargé seulement après consentement \(_legal_global\.py\) -->\s*'
                   r'<script id="ga-consent">.*?</script>', lambda m: GA_BLOCK, s, count=1, flags=re.S)
    else:
        s = OLD_GA.sub(lambda m: GA_BLOCK + (('\n<script>' + m.group(1) + '</script>') if m.group(1).strip() else ''), s, count=1)
    if ACCEPT_NEW not in s:
        s = s.replace(ACCEPT_OLD, ACCEPT_NEW)
    # 2. Lien CGU dans le footer
    if '/cgu.html">Conditions' not in s:
        s = re.sub(r'(<li><a href="/?confidentialite(?:\.html)?">Confidentialité</a></li>)',
                   r'\1\n          ' + CGU_LI, s, count=1)
    # 3. Pas de dollar
    s = s.replace(DOLLAR, EURO)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def targets():
    return glob.glob('*.html') + glob.glob('villes/*.html') + glob.glob('blog/*.html')


if __name__ == '__main__':
    n = sum(apply(f) for f in targets())
    print(f'{n} page(s) mises à jour')
