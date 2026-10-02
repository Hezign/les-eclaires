"""Sommaire latéral collant (sticky) + surlignage de la section en cours
pour les pages légales. Idempotent : relancer après toute modif du texte.

    python3 _legal_toc.py            # mentions-legales.html + confidentialite.html
    python3 _legal_toc.py page.html  # une page précise
"""
import re
import sys
import unicodedata

PAGES = ['mentions-legales.html', 'confidentialite.html']

CSS = '''<style id="legal-toc-css">
/* overflow-x:hidden sur html/body en fait des conteneurs de défilement : le sticky ne colle plus. clip coupe pareil sans casser le sticky. */
html,body{overflow-x:clip}
.page.has-toc{max-width:1120px}
.legal-layout{display:grid;grid-template-columns:240px minmax(0,1fr);gap:56px;align-items:start}
.legal-layout .prose{max-width:720px}
.legal-toc{position:sticky;top:calc(var(--topbar-h,0px) + 104px);max-height:calc(100vh - var(--topbar-h,0px) - 128px);overflow-y:auto;padding:4px 0}
.legal-toc-title{font-family:var(--ff-h);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--c-muted);margin:0 0 14px}
.legal-toc ol{list-style:none;margin:0;padding:0;border-left:1px solid var(--c-border2)}
.legal-toc li{margin:0}
.legal-toc a{display:flex;gap:10px;padding:7px 0 7px 16px;margin-left:-1px;border-left:2px solid transparent;font-size:14px;line-height:1.4;color:var(--c-muted);text-decoration:none;transition:color .2s,border-color .2s}
.legal-toc a .n{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;opacity:.7;min-width:18px;padding-top:1px}
.legal-toc a:hover{color:var(--c-ink)}
.legal-toc a.is-active{color:var(--c-ink);font-weight:600;border-left-color:var(--c-vert)}
.legal-layout .prose h2{scroll-margin-top:calc(var(--topbar-h,0px) + 100px)}
.legal-toc-mobile{display:none}
@media(max-width:960px){
  .legal-layout{grid-template-columns:minmax(0,1fr);gap:0}
  .legal-toc{display:none}
  .legal-toc-mobile{display:block;margin:0 0 32px;border:1px solid var(--c-border2);border-radius:14px;background:var(--c-bg2)}
  .legal-toc-mobile summary{cursor:pointer;padding:14px 18px;font-family:var(--ff-h);font-weight:700;font-size:15px;color:var(--c-ink);list-style:none;display:flex;justify-content:space-between;align-items:center}
  .legal-toc-mobile summary::-webkit-details-marker{display:none}
  .legal-toc-mobile summary::after{content:"+";font-size:20px;line-height:1;color:var(--c-muted)}
  .legal-toc-mobile[open] summary::after{content:"\\2212"}
  .legal-toc-mobile ol{margin:0;padding:0 18px 14px 18px;list-style:none}
  .legal-toc-mobile a{display:flex;gap:10px;padding:8px 0;font-size:14px;color:var(--c-mid);text-decoration:none;border-top:1px solid var(--c-border)}
  .legal-toc-mobile a .n{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;opacity:.7;min-width:18px}
}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
</style>'''

JS = '''<script id="legal-toc-js">
(function(){
  var links=[].slice.call(document.querySelectorAll('.legal-toc a'));
  var heads=[].slice.call(document.querySelectorAll('.legal-layout .prose h2[id]'));
  if(!links.length||!heads.length)return;
  var byId={};links.forEach(function(a){byId[a.getAttribute('href').slice(1)]=a;});
  var ticking=false;
  function update(){
    ticking=false;
    // section en cours = dernier titre passé sous le haut de l'écran (menu fixe compris)
    var cur=heads[0],line=window.innerHeight*0.3;
    heads.forEach(function(h){if(h.getBoundingClientRect().top<=line)cur=h;});
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)cur=heads[heads.length-1];
    links.forEach(function(a){a.classList.toggle('is-active',a===byId[cur.id]);});
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(update);}},{passive:true});
  window.addEventListener('resize',update);
  update();
})();
</script>'''


def slugify(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def strip_tags(t):
    return re.sub(r'<[^>]+>', '', t).strip()


def build(path):
    s = open(path, encoding='utf-8').read()
    orig = s

    # 1. Repartir d'un état propre (idempotence)
    s = re.sub(r'<style id="legal-toc-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="legal-toc-js">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<details class="legal-toc-mobile">.*?</details>\s*', '', s, flags=re.S)
    s = re.sub(r'<div class="legal-layout"><aside class="legal-toc".*?</aside>\s*', '', s, flags=re.S)
    s = s.replace('class="page has-toc"', 'class="page"')

    # 2. ids sur les h2 de la prose
    m = re.search(r'<div class="prose">(.*?)\n\s*</div>(?:<!--/legal-layout--></div>)?\n</div>\n<footer', s, re.S)
    if not m:
        print('skip (structure inattendue)', path)
        return False
    prose = m.group(1)
    items = []

    def add_id(mh):
        attrs, txt = mh.group(1), mh.group(2)
        label = strip_tags(txt)
        num = ''
        mn = re.match(r'(\d+)\.\s*(.*)', label)
        if mn:
            num, label = mn.group(1), mn.group(2)
        hid = slugify(label)
        attrs = re.sub(r'\s*id="[^"]*"', '', attrs)
        items.append((hid, num, label))
        return f'<h2{attrs} id="{hid}">{txt}</h2>'

    prose = re.sub(r'<h2([^>]*)>(.*?)</h2>', add_id, prose, flags=re.S)

    def li(cls=''):
        return ''.join(
            f'<li><a href="#{h}"><span class="n">{n}</span><span>{l}</span></a></li>'
            for h, n, l in items)

    aside = ('<div class="legal-layout"><aside class="legal-toc" aria-label="Sommaire">'
             '<p class="legal-toc-title">Sommaire</p>'
             f'<ol>{li()}</ol></aside>\n')
    mobile = ('<details class="legal-toc-mobile"><summary>Sommaire</summary>'
              f'<ol>{li()}</ol></details>\n  ')
    new_block = f'{aside}  <div class="prose">{mobile}{prose}\n</div><!--/legal-layout--></div>\n</div>\n<footer'
    s = s[:m.start()] + new_block + s[m.end():]
    s = s.replace('<div class="page">', '<div class="page has-toc">', 1)

    # 3. CSS + JS
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('</body>', JS + '\n</body>', 1)

    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        print('maj ', path, f'({len(items)} sections)')
        return True
    print('skip', path)
    return False


if __name__ == '__main__':
    for p in (sys.argv[1:] or PAGES):
        build(p)
    import _typo, _ds_shared
    for f in (sys.argv[1:] or PAGES):
        _ds_shared.apply(f); _typo.apply(f)
