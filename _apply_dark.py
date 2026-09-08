#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique le mode sombre (toggle clair/sombre) à une page.
Idempotent. Découple les tokens (band/menthe/vert-txt) + injecte le thème,
le script d'init (sans flash), le bouton toggle dans le nav et le JS.
Appelé par les build scripts (durabilité) et exécutable en direct :
    python3 _apply_dark.py            # toutes les pages
"""
import glob

THEME_CSS = '''<style id="theme-tokens">
:root{--c-band:#000000;--c-menthe:#E6FFF5;--c-vert-txt:#007A50}
html[data-theme="dark"]{
--c-bg:#0B0F0D;--c-bg2:#151B18;--c-bg3:#0F1512;
--c-ink:#EAF0EC;--c-text:#E3E9E5;--c-mid:#AEB6B1;--c-muted:#8A928D;
--c-border:rgba(255,255,255,.10);--c-border2:rgba(255,255,255,.16);
--c-vert:#00E58F;--c-vert-lt:#00F5A0;--c-vert-bg:rgba(0,242,160,.12);--c-vert-br:rgba(0,242,160,.30);
--c-jaune:#00E58F;--c-jaune-lt:#00F5A0;
--c-band:#1B231F;--c-menthe:#10201A;--c-vert-txt:#3DEBAE}
html[data-theme="dark"] body{background:var(--c-bg);color:var(--c-text)}
html[data-theme="dark"] nav{background:rgba(20,26,23,.92)!important;border-color:var(--c-border2)!important}
html[data-theme="dark"] #preloader{background:#0B0F0D!important}
html[data-theme="dark"] .btn-primary{background:var(--c-vert-lt)!important;color:#05231a!important}
html[data-theme="dark"] .stats-wrap,html[data-theme="dark"] .process-wrap{border-top:1px solid var(--c-border);border-bottom:1px solid var(--c-border)}
.theme-toggle{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;border:1px solid var(--c-border2);background:transparent;color:var(--c-ink);cursor:pointer;flex-shrink:0;transition:background .2s,border-color .2s;margin-left:4px}
.theme-toggle:hover{background:var(--c-vert-bg);border-color:var(--c-vert-br)}
.theme-toggle svg{width:18px;height:18px}
.theme-toggle .moon{display:none}
html[data-theme="dark"] .theme-toggle .moon{display:block}
html[data-theme="dark"] .theme-toggle .sun{display:none}
</style>'''

THEME_INIT = '<script>(function(){try{var K="les-eclaires-theme",t=localStorage.getItem(K);if(!t)t="light";document.documentElement.setAttribute("data-theme",t);}catch(e){}})();</script>'

TOGGLE_BTN = '''<button class="theme-toggle" id="themeToggle" aria-label="Basculer clair/sombre" title="Thème clair/sombre"><svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>'''

TOGGLE_JS = '<script>/*theme-toggle-js*/document.addEventListener("click",function(e){var b=e.target.closest("#themeToggle");if(!b)return;var r=document.documentElement,n=r.getAttribute("data-theme")==="dark"?"light":"dark";r.setAttribute("data-theme",n);try{localStorage.setItem("les-eclaires-theme",n)}catch(e){}});</script>'


def apply(path):
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    o = s
    # 1) Découplage tokens (nécessaire pour que le sombre fonctionne)
    s = s.replace('background:var(--c-ink)', 'background:var(--c-band)')
    s = s.replace('#E6FFF5', 'var(--c-menthe)')
    s = s.replace('#007A50', 'var(--c-vert-txt)')
    # 2) Thème + init (avant </head>, après le CSS pour éviter le flash)
    if 'theme-tokens' not in s and '</head>' in s:
        s = s.replace('</head>', THEME_CSS + '\n' + THEME_INIT + '\n</head>', 1)
    # 3) Bouton toggle dans le nav
    if 'id="themeToggle"' not in s and '<button class="nav-burger"' in s:
        s = s.replace('<button class="nav-burger"', TOGGLE_BTN + '\n  <button class="nav-burger"', 1)
    # 4) JS du toggle
    if '/*theme-toggle-js*/' not in s and '</body>' in s:
        s = s.replace('</body>', TOGGLE_JS + '\n</body>', 1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
    return True


if __name__ == '__main__':
    files = [f for f in glob.glob('*.html') if not f.endswith(('-preview.html',))]
    files += glob.glob('blog/*.html') + glob.glob('villes/*.html')
    for f in files:
        apply(f)
    print(f"{len(files)} pages : mode sombre appliqué")
