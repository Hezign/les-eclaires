#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Règles légales et de marque appliquées à TOUTES les pages (accueil compris).
Idempotent. Appelé par _apply_dark.apply() ; exécutable en direct :

    python3 _legal_global.py

1. Google Analytics chargé UNIQUEMENT après acceptation des cookies (plus de
   script Google ni de signal sans cookie avant le choix). Cookies _ga limités à
   13 mois (recommandation CNIL ; défaut Google = 2 ans).
2. Footer identique sur toutes les pages (FOOTER_TOP / FOOTER_BOTTOM).
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

# Footer unique du site (référence : accueil, liste validée par Harry le 02/10/2026).
FOOTER_TOP = """<div class="footer-top">
    <div class="footer-cols">
      <div class="footer-col">
        <h4>Le service</h4>
        <ul>
          <li><a href="/simulateur">Simulateur IRVE</a></li>
          <li><a href="/copropriete">Bornes en copropriété</a></li>
          <li><a href="/entreprise">Bornes en entreprise</a></li>
          <li><a href="/partenaires.html">Devenir partenaire</a></li>
          <li><a href="/#histoire">Notre histoire</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Ressources</h4>
        <ul>
          <li><a href="/blog/">Blog IRVE</a></li>
          <li><a href="https://advenir.mobi/" target="_blank" rel="noopener">Prime ADVENIR ↗</a></li>
          <li><a href="https://www.avere-france.org/" target="_blank" rel="noopener">AVERE-France ↗</a></li>
          <li><a href="https://www.qualifelec.fr/" target="_blank" rel="noopener">Qualifelec ↗</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations</h4>
        <ul>
          <li><a href="/mentions-legales.html">Mentions légales</a></li>
          <li><a href="/confidentialite.html">Confidentialité</a></li>
          <li><a href="/cgu.html">Conditions d'utilisation</a></li>
          <li><a href="mailto:contact@leseclaires.fr">Nous écrire</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-cities">
      <h4>Guides par ville</h4>
      <ul class="footer-cities-list">
          <li><a href="/villes/borne-recharge-aix-en-provence.html">Borne de recharge Aix-en-Provence</a></li>
          <li><a href="/villes/borne-recharge-annecy.html">Borne de recharge Annecy</a></li>
          <li><a href="/villes/borne-recharge-lyon.html">Borne de recharge Lyon</a></li>
          <li><a href="/villes/borne-recharge-nantes.html">Borne de recharge Nantes</a></li>
          <li><a href="/villes/borne-recharge-bordeaux.html">Borne de recharge Bordeaux</a></li>
          <li><a href="/villes/borne-recharge-montpellier.html">Borne de recharge Montpellier</a></li>
          <li><a href="/villes/borne-recharge-toulouse.html">Borne de recharge Toulouse</a></li>
          <li><a href="/villes/borne-recharge-rennes.html">Borne de recharge Rennes</a></li>
          <li><a href="/villes"><strong>Toutes les villes →</strong></a></li>
      </ul>
    </div>
  </div>"""

FOOTER_BOTTOM = """<div class="footer-bottom">
    <span class="footer-brand-group" style="display:inline-flex;align-items:center;gap:10px"><img class="footer-bottom-logo" src="/logo-eclaires.svg" alt="Les Éclairés" width="24" height="24" style="height:24px;width:auto;border-radius:6px;display:block;flex-shrink:0"><span class="f-brand-name">Les Éclairés</span></span>
    <span class="footer-legal">© 2026 Les Éclairés · Comprendre, choisir, installer.</span>
    <a class="footer-linkedin" href="https://www.linkedin.com/company/les-%C3%A9clair%C3%A9s/" target="_blank" rel="noopener" aria-label="LinkedIn Les Éclairés"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
  </div>"""


def _block(s, start, pos=0):
    """Renvoie (début, fin) du <div> commençant par `start` (div imbriqués compris)."""
    a = s.find(start, pos)
    if a == -1:
        return None
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return a, a + m.end()
    return None


def unify_footer(s, path):
    f = s.find('<footer')
    if f == -1:
        return s
    for start, html in (('<div class="footer-top">', FOOTER_TOP), ('<div class="footer-bottom">', FOOTER_BOTTOM)):
        r = _block(s, start, f)
        if r:
            s = s[:r[0]] + html + s[r[1]:]
    # la page courante n'est pas un lien vers elle-même
    href = '/' + path.replace(os.sep, '/')
    f = s.find('<footer')
    s = s[:f] + s[f:].replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">')
    return s


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
    # 2. Footer identique partout (colonnes, villes, mentions)
    s = unify_footer(s, path)
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
