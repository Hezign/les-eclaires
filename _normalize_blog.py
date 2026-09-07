#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalise un/des article(s) de blog sur la DA + le header du site.
À LANCER APRÈS CHAQUE PUBLICATION n8n (le pipeline peut sortir du HTML hors DA) :

    python3 _normalize_blog.py                 # tout le dossier blog/
    python3 _normalize_blog.py blog/mon-article.html   # un fichier précis

Idempotent : réexécutable sans dommage. Applique polices, couleurs DA, logo SVG,
footer (séparateur retiré + LinkedIn + texte foncé), Consent Mode v2, contraste AA,
et le header complet (topbar + nav + cookie) via _inject_header.
"""
import re, sys, glob
import _inject_header  # header/topbar/cookie complet

FONTS = ("family=Schibsted+Grotesk:wght@400;500;600;700;800"
         "&family=Manrope:wght@300;400;500;600;700"
         "&family=JetBrains+Mono:wght@400;500&display=swap")

COLORS = [  # (regex, remplacement) - ancienne DA -> nouvelle
    (r'#00A96E', '#00C27E'), (r'#00C97F', '#00F5A0'), (r'#00935[fF]', '#00C27E'),
    (r'0,169,110', '0,194,126'), (r'#F8F6F1', '#F4F6F5'), (r'#F0EDE6', '#E6FFF5'),
    (r'#111110', '#000000'), (r'#2C2C28', '#1A1D1B'), (r'#888884', '#5C6560'),
    (r'#6B6B66', '#5C6560'), (r'#55554F', '#454B48'),
]

GA_HEAD = ('<!-- Google tag (gtag.js) -->\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZXGFCVHHDM"></script>\n'
    '<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n'
    "  gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});\n"
    "  try{if(localStorage.getItem('les-eclaires-cookie-v2')==='y')gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}catch(e){}\n"
    "  gtag('js', new Date());\n  gtag('config', 'G-ZXGFCVHHDM');\n</script>")

LINK = ('<a class="footer-linkedin" href="https://www.linkedin.com/company/les-%C3%A9clair%C3%A9s/" '
        'target="_blank" rel="noopener" aria-label="LinkedIn Les Éclairés"><svg viewBox="0 0 24 24" fill="currentColor" '
        'aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>')


def normalize(path):
    s = open(path, encoding='utf-8').read()
    o = s
    # Polices
    s = re.sub(r'family=[^"]*display=swap', FONTS, s)
    s = s.replace('Bricolage Grotesque', 'Schibsted Grotesk').replace("'Inter'", "'Manrope'")
    # Couleurs DA
    for pat, rep in COLORS:
        s = re.sub(pat, rep, s, flags=re.IGNORECASE)
    # Logo base64 -> SVG hébergé
    s = re.sub(r'<img class="nav-logo-img" src="data:[^"]*"[^>]*>',
               '<img class="nav-logo-img" src="/logo-eclaires.svg" alt="Les Éclairés" width="30" height="30">', s)
    s = re.sub(r'<img class="footer-bottom-logo" src="data:[^"]*"[^>]*>',
               '<img class="footer-bottom-logo" src="/logo-eclaires.svg" alt="Les Éclairés" width="24" height="24" style="height:24px;width:auto;border-radius:6px;display:block;flex-shrink:0">', s)
    # Footer : séparateur retiré + LinkedIn + texte foncé
    s = s.replace('padding-bottom:40px;border-bottom:1px solid var(--c-border)}', 'padding-bottom:40px}')
    s = s.replace('footer .footer-bottom .f-brand-name{font-family:var(--ff-h);font-size:16px;font-weight:800;color:#fff;letter-spacing:-0.04em}',
                  'footer .footer-bottom .f-brand-name{font-family:var(--ff-h);font-size:16px;font-weight:800;color:#08130d;letter-spacing:-0.04em}')
    s = s.replace('footer .footer-bottom .footer-legal{font-size:12px;color:rgba(255,255,255,.9);font-weight:300;margin:0}',
                  'footer .footer-bottom .footer-legal{font-size:12px;color:rgba(0,0,0,.6);font-weight:300;margin:0}')
    anchor = '<span class="footer-legal">© 2026 Les Éclairés · Comprendre, choisir, installer.</span>'
    if 'footer-linkedin' not in s and anchor in s:
        s = s.replace(anchor, anchor + '\n    ' + LINK, 1)
    # Consent Mode : ajoute GA si absent, sinon convertit le gtag('js') existant
    if 'googletagmanager' not in s and '<head>' in s:
        s = s.replace('<head>', '<head>' + GA_HEAD, 1)
    elif "gtag('consent','default'" not in s:
        s = s.replace("gtag('js', new Date());",
                      "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});"
                      "try{if(localStorage.getItem('les-eclaires-cookie-v2')==='y')gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}catch(e){}\n  gtag('js', new Date());", 1)
    # Contraste AA surtitres
    s = re.sub(r'(\.section-tag\{[^}]*?)color:var\(--c-vert\)', r'\1color:#007A50', s)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
    # Header complet + topbar + cookie (idempotent)
    _inject_header.inject_file(path)
    return True


if __name__ == '__main__':
    targets = sys.argv[1:] or [f for f in glob.glob('blog/*.html') if not f.endswith('template.html')]
    for f in targets:
        normalize(f)
    print(f"{len(targets)} article(s) normalisé(s) sur la DA + header")
