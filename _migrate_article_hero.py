#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migration ONE-SHOT des articles du vieux gabarit `.article-hero` (colonne centrée,
pas de sommaire) vers le gabarit d'article unique `.hero` (photo plein cadre,
colonne + sommaire latéral), celui des articles n8n.

Garde le <head> de l'article (title, metas, JSON-LD, GA, header injecté), retire
ses règles CSS .prose/.article-*, ajoute le CSS article du gabarit de référence,
reconstruit hero + layout + sommaire + CTA. Ne touche pas au texte de l'article.

    python3 _migrate_article_hero.py   # les articles .article-hero restants
"""
import glob
import html
import re
import unicodedata

REF = 'blog/zaptec-ou-hager-borne-copropriete.html'
KEEP = ('#pgbar', '.hero', '.badge', '.htitle', '.hmeta', '.dot', '.layout', '.sidebar',
        '.toc', '.scta', '.prose', '.ctafin', '.bg', '.bd')

TOC_JS = ('<script>(function(){var b=document.getElementById("pgbar");var tl=document.querySelectorAll("#tocl a");'
          'window.addEventListener("scroll",function(){var s=document.documentElement.scrollTop;'
          'var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;'
          'b.style.width=(h>0?Math.min(100,s/h*100):0)+"%";var hs=document.querySelectorAll(".prose h2[id]");'
          'var cur="";hs.forEach(function(x){if(window.scrollY>=x.offsetTop-90)cur=x.id;});'
          'tl.forEach(function(a){a.classList.toggle("on",a.getAttribute("href")==="#"+cur);});},{passive:true});})();</script>')


def slugify(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60]


def strip_tags(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()


def article_css():
    s = open(REF, encoding='utf-8').read()
    st = re.findall(r'<style>(.*?)</style>', s, re.S)[0]
    out = []
    # règles de premier niveau
    top = re.sub(r'@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', st)
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', top):
        if any(k in sel for k in KEEP):
            out.append(f'{sel.strip()}{{{body}}}')
    # media queries : ne garder que les règles article
    for mq, inner in re.findall(r'(@media[^{]*)\{((?:[^{}]*\{[^{}]*\})*)[^{}]*\}', st):
        rules = [f'{sel.strip()}{{{b}}}' for sel, b in re.findall(r'([^{}]+)\{([^{}]*)\}', inner)
                 if any(k in sel for k in KEEP)]
        if rules:
            out.append(mq.replace('@media@media', '@media').strip() + '{' + ''.join(rules) + '}')
    return '<style id="article-base">\n' + '\n'.join(out) + '\n</style>'


def drop_old_rules(s):
    def clean(m):
        tag, st = m.group(1), m.group(2)
        if 'id=' in tag:            # blocs injectés (header, thème, cover...) : intacts
            return m.group(0)
        st = re.sub(r'[^{}]*(?:\.prose|\.article-|\.btn-cta|\.toc-mini)[^{}]*\{[^{}]*\}', '', st)
        return f'{tag}{st}</style>'
    return re.sub(r'(<style[^>]*>)(.*?)</style>', clean, s, flags=re.S)


def migrate(path, css):
    s = open(path, encoding='utf-8').read()
    if 'class="article-wrap"' not in s:
        return False
    tag = strip_tags(re.search(r'<div class="article-tag">(.*?)</div>', s, re.S).group(1))
    h1 = re.search(r'<h1 class="article-title">(.*?)</h1>', s, re.S).group(1).strip()
    date = strip_tags(re.search(r'<p class="article-date"[^>]*>(.*?)</p>', s, re.S).group(1))
    img = re.search(r'<div class="article-hero has-photo"><img src="([^"]+)" alt="([^"]*)"', s)
    m_prose = re.search(r'<div class="prose">(.*?)</div>\s*<div class="article-cta">', s, re.S)
    prose = m_prose.group(1)
    cta = re.search(r'<div class="article-cta">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', s, re.S)

    prose = re.sub(r'<div class="toc-mini".*?</div>\s*', '', prose, count=1, flags=re.S)
    toc, seen = [], set()

    def h2id(m):
        attrs, txt = m.group(1), m.group(2)
        mid = re.search(r'id="([^"]+)"', attrs)
        hid = mid.group(1) if mid else slugify(strip_tags(txt))
        while hid in seen:
            hid += '-2'
        seen.add(hid)
        toc.append((hid, strip_tags(txt)))
        if not mid:
            attrs = f'{attrs} id="{hid}"'
        return f'<h2{attrs}>{txt}</h2>'
    prose = re.sub(r'<h2([^>]*)>(.*?)</h2>', h2id, prose, flags=re.S)

    words = len(strip_tags(prose).split())
    mins = max(2, round(words / 220))
    toc_html = ''.join(f'<li><a href="#{h}">{html.escape(t, quote=False)}</a></li>' for h, t in toc)
    body = (
        '<div id="pgbar"></div>\n'
        f'<div class="hero has-photo"><img class="hero-bg" src="{img.group(1)}" alt="{img.group(2)}" '
        'loading="eager" fetchpriority="high" width="1400" height="620"><span class="hero-scrim"></span><div class="hero-in">\n'
        f'<div class="badge">{tag}</div>\n<h1 class="htitle">{h1}</h1>\n'
        f'<div class="hmeta"><span>{date}</span><span class="dot"></span><span>{mins} min de lecture</span>'
        '<span class="dot"></span><span>Les Éclairés</span></div>\n</div></div>\n'
        '<div class="layout">\n<main><div class="prose">' + prose + '</div>\n'
        f'<div class="ctafin"><h2>{cta.group(1)}</h2><p>{cta.group(2)}</p>\n'
        '<a href="/simulateur" class="bg">Démarrer le simulateur →</a>\n'
        '<a href="/partenaires.html" class="bd">Trouver un installateur</a></div></main>\n'
        '<aside class="sidebar">\n'
        f'<div class="toc"><h3>Sommaire</h3><ul id="tocl">{toc_html}</ul></div>\n'
        '<div class="scta"><p>Pas sûr de quelle borne vous avez besoin ?</p>'
        '<a href="/simulateur">Simulateur gratuit →</a><a href="/partenaires.html" class="s">Trouver un installateur</a></div>\n'
        '</aside></div>\n'
    )
    start = s.find('<div class="article-wrap">')
    end = s.find('<footer', start)
    s = s[:start] + body + '\n' + s[end:]
    s = drop_old_rules(s)
    s = re.sub(r'<style id="article-base">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', css + '\n</head>', 1)
    s = s.replace('</footer>', '</footer>\n' + TOC_JS, 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('migré', path, f'({len(toc)} sections, {mins} min)')
    return True


if __name__ == '__main__':
    css = article_css()
    for f in sorted(glob.glob('blog/*.html')):
        migrate(f, css)
