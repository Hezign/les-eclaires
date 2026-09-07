#!/usr/bin/env python3
# Injecte la topbar partenaire + la bulle cookie sur les pages du site.
# Pour les pages blog : remplace aussi le nav réduit par le HEADER COMPLET du site.
# Idempotent (détecte class="topbar"). Réexécutable après un rebuild.
import re

_IDX = open('index.html', encoding='utf-8').read()
_NAV_FULL = re.search(r'<nav>.*?</nav>', _IDX, re.S).group(0)
# Header complet adapté aux sous-pages (liens absolus vers l'accueil)
NAV_BLOG = (_NAV_FULL
    .replace('<a class="nav-logo" href="#">', '<a class="nav-logo" href="/">')
    .replace('href="#pourquoi"', 'href="/#pourquoi"')
    .replace('href="#histoire"', 'href="/#histoire"')
    .replace('href="#faq"', 'href="/#faq"')
    .replace('href="#partenaires"', 'href="/partenaires.html"'))

TOPBAR = '''<!-- TOPBAR PARTENAIRE -->
<div class="topbar" id="topbar">
  <a class="tb-link" href="/partenaires.html">
    <svg class="tb-bolt" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2L4 13.5h6.2L9 22l9-12.5h-6.2L13 2z"/></svg>
    <span class="tb-txt"><strong>Vous &#234;tes installateur IRVE&nbsp;?</strong> Recevez des demandes qualifi&#233;es, sans prospecter.</span>
  </a>
  <button class="tb-close" aria-label="Fermer le bandeau" onclick="this.closest('.topbar').classList.add('hidden');document.body.classList.add('tb-off')">&times;</button>
</div>'''

COOKIE = '''<!-- COOKIE BANNER -->
<div class="cookie-banner" id="cookieBanner">
  <p>&#x1F36A; <strong>Cookies</strong> : On utilise des cookies pour analyser l'audience et am&#233;liorer votre exp&#233;rience. Aucune donn&#233;e n'est revendue &#224; des tiers.</p>
  <div class="cookie-btns">
    <button class="cookie-accept" id="btnAccept">Accepter</button>
    <button class="cookie-decline" id="btnDecline">Refuser</button>
  </div>
</div>
<button class="cookie-fab" id="cookieFab" aria-label="Pr&#233;f&#233;rences cookies" title="Pr&#233;f&#233;rences cookies">&#x1F36A;</button>'''

CSS_COMMON = '''<style>
/* Topbar partenaire + cookies (injecté) */
:root{--topbar-h:40px;--c-vert-lt:#00F5A0}
.topbar{position:fixed;top:0;left:0;width:100%;height:var(--topbar-h);z-index:300;background:var(--c-ink);color:#fff;display:flex;align-items:center;justify-content:center;gap:14px;overflow:hidden;padding:0 44px 0 20px;font-family:var(--ff-b);font-size:13.5px;font-weight:400;transition:transform .35s cubic-bezier(0.16,1,0.3,1)}
.topbar.hidden{transform:translateY(-100%)}
.topbar .tb-link{display:inline-flex;align-items:center;gap:12px;color:#fff;text-decoration:none;overflow:hidden;min-width:0}
.topbar .tb-link:hover .tb-txt{text-decoration:underline}
.topbar .tb-bolt{width:14px;height:14px;color:var(--c-vert-lt);flex-shrink:0}
.topbar .tb-txt{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.topbar .tb-txt strong{font-weight:600;color:#fff}
.topbar .tb-close{position:absolute;right:14px;top:50%;transform:translateY(-50%);width:22px;height:22px;border:none;background:transparent;color:rgba(255,255,255,.55);cursor:pointer;font-size:18px;line-height:1;border-radius:50%}
.topbar .tb-close:hover{color:#fff;background:rgba(255,255,255,.12)}
nav{top:calc(var(--topbar-h) + 12px)!important;transition:top .35s cubic-bezier(0.16,1,0.3,1)}
body.tb-off nav{top:16px!important}
html{scroll-padding-top:calc(var(--topbar-h) + 90px)}
.cookie-banner{position:fixed;bottom:24px;left:24px;z-index:500;max-width:360px;background:var(--c-ink);color:rgba(255,255,255,.75);border-radius:16px;padding:20px 22px;box-shadow:0 8px 32px rgba(0,0,0,.25);transform:translateY(200px);opacity:0;transition:transform .5s cubic-bezier(0.16,1,0.3,1),opacity .5s;pointer-events:none;font-family:var(--ff-b)}
.cookie-banner.show{transform:translateY(0);opacity:1;pointer-events:auto}
.cookie-banner p{font-size:13px;line-height:1.6;margin-bottom:14px}
.cookie-banner strong{color:#fff;font-weight:600}
.cookie-btns{display:flex;gap:8px}
.cookie-accept{font-family:var(--ff-h);font-size:13px;font-weight:600;background:var(--c-vert);color:#0a0a09;border:none;border-radius:999px;padding:8px 18px;cursor:pointer}
.cookie-decline{font-family:var(--ff-h);font-size:13px;font-weight:500;background:transparent;color:rgba(255,255,255,.45);border:1px solid rgba(255,255,255,.15);border-radius:999px;padding:8px 16px;cursor:pointer}
.cookie-fab{position:fixed;bottom:24px;left:24px;z-index:499;width:46px;height:46px;border-radius:50%;background:var(--c-ink);color:#fff;border:none;cursor:pointer;font-size:20px;line-height:1;display:none;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.22)}
.cookie-fab.show{display:flex}
@media(max-width:640px){.cookie-banner{left:12px;right:12px;max-width:none;bottom:12px}.cookie-fab{bottom:12px;left:12px}}
@media(max-width:560px){.topbar .tb-txt strong{display:none}}
/* dégage le contenu sous le header + topbar (mobile) */
@media(max-width:640px){.page,.hero-city{padding-top:calc(var(--topbar-h) + 76px)!important}}
</style>'''

CSS_BLOG = '''<style>
/* Header complet du site (injecté sur les pages blog) */
nav{position:fixed;top:calc(var(--topbar-h) + 12px);left:50%;transform:translateX(-50%);z-index:200;height:56px;width:calc(100% - 48px);max-width:1100px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;background:rgba(244,246,245,0.96);-webkit-backdrop-filter:blur(24px) saturate(1.4);backdrop-filter:blur(24px) saturate(1.4);border:1px solid var(--c-border2);border-radius:100px;box-shadow:0 4px 24px rgba(0,0,0,.07)}
.nav-logo{display:flex;align-items:center;gap:10px;text-decoration:none}
.nav-logo-img{height:30px;width:auto;display:block;flex-shrink:0;object-fit:contain;border-radius:8px}
.nav-logo-text{font-family:var(--ff-h);font-size:16px;font-weight:700;color:var(--c-ink);letter-spacing:-0.03em;white-space:nowrap}
.nav-links{display:flex;align-items:center;gap:40px;list-style:none;margin:0;padding:0}
.nav-links a{font-size:14px;font-weight:400;color:var(--c-muted);transition:color .18s;text-decoration:none}
.nav-links a:hover{color:var(--c-ink)}
.btn-nav{font-family:var(--ff-h);font-size:13.5px;font-weight:600;background:var(--c-vert-lt);color:#0a0a09;padding:9px 20px;border-radius:999px;border:none;cursor:pointer;letter-spacing:-0.02em;white-space:nowrap;text-decoration:none}
.nav-burger{display:none;flex-direction:column;justify-content:center;gap:5px;width:42px;height:42px;background:none;border:none;cursor:pointer;padding:9px;margin-left:4px}
.nav-burger span{display:block;width:24px;height:2px;background:var(--c-ink);border-radius:2px;transition:transform .25s,opacity .2s}
@media(max-width:600px){.btn-nav{display:none}}
@media(max-width:820px){
.nav-links{display:none}
.nav-burger{display:flex}
nav.open .nav-links{display:flex;flex-direction:column;align-items:stretch;gap:2px;position:absolute;top:calc(100% + 12px);left:0;right:0;background:var(--c-bg2);border:1px solid var(--c-border2);border-radius:20px;padding:14px;box-shadow:0 16px 44px rgba(0,0,0,.14)}
nav.open .nav-links li{list-style:none}
nav.open .nav-links li a{display:block;padding:13px 16px;border-radius:12px;font-size:15px;color:var(--c-ink)}
nav.open .nav-links li a:hover{background:var(--c-vert-bg)}
nav.open .nav-burger span:nth-child(1){transform:translateY(7px) rotate(45deg)}
nav.open .nav-burger span:nth-child(2){opacity:0}
nav.open .nav-burger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
}
/* dégage le contenu article sous le header + topbar */
.article-wrap{padding-top:calc(var(--topbar-h) + 92px)!important}
@media(max-width:640px){.article-wrap{padding-top:calc(var(--topbar-h) + 72px)!important}}
</style>'''

JS_COOKIE = '''<script>
(function(){var CK='les-eclaires-cookie-v2';function el(i){return document.getElementById(i);}
function showFab(){var f=el('cookieFab');if(f)f.classList.add('show');}
function openC(){var b=el('cookieBanner');if(b)b.classList.add('show');var f=el('cookieFab');if(f)f.classList.remove('show');}
function closeC(ok){var b=el('cookieBanner');if(b)b.classList.remove('show');try{localStorage.setItem(CK,ok?'y':'n');}catch(e){}showFab();}
try{if(!localStorage.getItem(CK)){setTimeout(openC,1800);}else{showFab();}}catch(e){setTimeout(openC,1800);}
var ba=el('btnAccept'),bd=el('btnDecline'),cf=el('cookieFab');
if(ba)ba.addEventListener('click',function(){closeC(true);});
if(bd)bd.addEventListener('click',function(){closeC(false);});
if(cf)cf.addEventListener('click',openC);})();
</script>'''

JS_BURGER = '''<script>
(function(){var nav=document.querySelector('nav');var b=document.getElementById('navBurger');if(!nav||!b)return;
function close(){nav.classList.remove('open');b.setAttribute('aria-expanded','false');}
b.addEventListener('click',function(e){e.stopPropagation();var o=nav.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});
document.addEventListener('click',function(e){if(nav.classList.contains('open')&&!nav.contains(e.target))close();});})();
</script>'''


def inject_file(path, is_blog=True):
    """Injecte topbar + cookie + HEADER COMPLET du site (nav identique partout)."""
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    if 'class="topbar"' in s:
        return False  # déjà injecté
    css = CSS_COMMON + '\n' + CSS_BLOG
    if '</head>' in s:
        s = s.replace('</head>', css + '\n</head>', 1)
    s = re.sub(r'<nav>.*?</nav>', lambda m: NAV_BLOG, s, count=1, flags=re.S)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + TOPBAR, s, count=1)
    tail = COOKIE + '\n' + JS_BURGER + '\n' + JS_COOKIE
    s = s.replace('</body>', tail + '\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    return True


def upgrade_nav(path):
    """Remplace un nav réduit/partiel par le header complet (pages déjà injectées)."""
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    if 'class="nav-links"' in s:
        return False  # déjà header complet
    s = re.sub(r'<nav>.*?</nav>', lambda m: NAV_BLOG, s, count=1, flags=re.S)
    if '</head>' in s and CSS_BLOG not in s:
        s = s.replace('</head>', CSS_BLOG + '\n</head>', 1)
    if 'navBurger' in s and JS_BURGER not in s:
        s = s.replace('</body>', JS_BURGER + '\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    return True


if __name__ == '__main__':
    import glob
    pages = ['partenaires.html', 'confidentialite.html', 'mentions-legales.html',
             '404.html', 'copropriete.html', 'villes.html'] + glob.glob('villes/*.html') + glob.glob('blog/*.html')
    n = 0
    for f in pages:
        if inject_file(f):
            n += 1
    print(f"{n} pages injectées (topbar + cookie + header complet)")
