#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sections « façon accueil » réutilisables par les pages intérieures.

La home (index.html) est la référence de la DA : hero en 2 colonnes avec carte de
recommandation et décor (grille + halos verts), bande noire de chiffres, sections
menthe avec cartes à bord supérieur vert et tuile noire, cartes contour avec gros
numéro pâle, bande noire d'étapes avec pastilles « ÉTAPE 01 », FAQ en 2 colonnes.

Ce module fournit le CSS (classes hs-*, injecté par _ds_shared) et des fonctions
qui rendent ces blocs ; les générateurs (_build_villes, _build_copro,
_build_partenaires) composent leurs pages avec.
"""

ICONS = {
    'home': '<path d="M3 10.5 12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    'building': '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    'percent': '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    'euro': '<path d="M18 7a7 7 0 1 0 0 10M4 10h10M4 14h10"/>',
    'calendar': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'bolt': '<path d="M13 2 4 13.5h6.2L9 22l9-12.5h-6.2z"/>',
    'map': '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    'scale': '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
}

ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" width="15" height="15" aria-hidden="true">'
         '<path d="M3 8h10M9 4l4 4-4 4"/></svg>')


def icon(name, size=22):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def hero(*, crumbs='', badge, h1, lead, ctas, mini=(), card=''):
    """crumbs = html du fil d'Ariane ; ctas = [(href, label, 'primary'|'ghost')] ;
    mini = [(valeur, libellé)] ; card = html de la carte de droite (reco_card)."""
    btns = ''.join(
        f'<a href="{h}" class="{"btn-primary" if k == "primary" else "hs-btn-ghost"}">{t}'
        f'{" " + ARROW if k == "primary" else ""}</a>' for h, t, k in ctas)
    minis = ''.join(f'<span><b>{v}</b> {t}</span>' for v, t in mini)
    return f'''<section class="hs-hero{' has-card' if card else ''}">
  <div class="hs-hero-deco" aria-hidden="true"></div>
  <div class="hs-wrap hs-hero-grid">
    <div class="hs-hero-text">
      {f'<div class="breadcrumb">{crumbs}</div>' if crumbs else ''}
      <div class="hs-badge"><span class="badge-dot"></span>{badge}</div>
      <h1>{h1}</h1>
      <p class="hs-hero-lead">{lead}</p>
      <div class="hs-ctas">{btns}</div>
      {f'<div class="hs-mini">{minis}</div>' if minis else ''}
    </div>
    {f'<div class="hs-hero-card">{card}</div>' if card else ''}
  </div>
</section>'''


def reco_card(title, pill, rows, foot):
    """rows = [(icone, libellé, valeur, libellé droit, valeur droite)]"""
    r = ''.join(
        f'<div class="hs-reco-row"><span class="hs-reco-ico">{icon(ic)}</span>'
        f'<div><div class="k">{k}</div><div class="v">{v}</div></div>'
        f'<div class="r"><div class="k">{k2}</div><div class="v">{v2}</div></div></div>'
        for ic, k, v, k2, v2 in rows)
    return (f'<div class="hs-reco"><div class="hs-reco-head"><span class="t">{title}</span>'
            f'<span class="hs-reco-pill">{pill}</span></div>{r}'
            f'<div class="hs-reco-foot">{icon("bolt", 15)}<span>{foot}</span></div></div>')


def section(inner, *, tone='white', tag='', h2='', lead='', sid='', cls=''):
    head = (f'<span class="section-tag">{tag}</span>' if tag else '') + \
           (f'<h2 class="hs-h2">{h2}</h2>' if h2 else '') + \
           (f'<p class="hs-lead">{lead}</p>' if lead else '')
    return (f'<section class="hs-sec hs-{tone}{(" " + cls) if cls else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>'
            f'<div class="hs-wrap">{head}{inner}</div></section>')


def top_cards(cards):
    """Cartes à bord supérieur vert + tuile noire (section « Pour qui » de la home).
    cards = [(icone, titre, montant|'' , texte)]"""
    return '<div class="hs-cards">' + ''.join(
        f'<div class="hs-card-top"><span class="hs-tile">{icon(ic, 24)}</span><h3>{t}</h3>'
        f'{f"<span class={chr(34)}amt{chr(34)}>{a}</span>" if a else ""}<p>{p}</p></div>'
        for ic, t, a, p in cards) + '</div>'


def num_cards(cards):
    """Cartes contour + icône contour + gros numéro pâle (section « Pourquoi » de la home).
    cards = [(icone, titre, texte)]"""
    return '<div class="hs-cards">' + ''.join(
        f'<div class="hs-card-num"><div class="hd"><span class="hs-ico-o">{icon(ic)}</span>'
        f'<span class="hs-num">{i:02d}</span></div><h3>{t}</h3><p>{p}</p></div>'
        for i, (ic, t, p) in enumerate(cards, 1)) + '</div>'


def steps(items):
    """Cartes d'étapes sur bande noire (section « Comment ça se passe » de la home).
    items = [(titre, texte)]"""
    return '<div class="hs-steps">' + ''.join(
        f'<div class="hs-step"><span class="hs-pill">ÉTAPE {i:02d}</span><h3>{t}</h3><p>{p}</p></div>'
        for i, (t, p) in enumerate(items, 1)) + '</div>'


def faq_section(tag, h2, lead, details_html, sid='faq'):
    """FAQ en 2 colonnes : titre à gauche, questions (details) à droite."""
    return (f'<section class="hs-sec hs-white" id="{sid}"><div class="hs-wrap hs-faq-grid">'
            f'<div><span class="section-tag">{tag}</span><h2 class="hs-h2">{h2}</h2>'
            f'<p class="hs-lead">{lead}</p></div><div class="faq-city">{details_html}</div></div></section>')


def cta_band(h, p, href, label):
    return (f'<section class="hs-sec hs-menthe hs-cta-sec"><div class="hs-wrap"><div class="hs-cta">'
            f'<h2>{h}</h2><p>{p}</p><a href="{href}" class="btn-primary">{label} {ARROW}</a></div></div></section>')


CSS = '''<style id="hs-css">
/* ===== Sections façon accueil (référence : index.html) ===== */
.hs-wrap{max-width:1032px;margin:0 auto;padding:0 24px;width:100%;box-sizing:border-box}
.hs-sec{padding:104px 0}
.hs-white{background:var(--c-bg2)}
.hs-grey{background:var(--c-bg)}
.hs-menthe{background:var(--c-menthe)}
.hs-band{background:var(--c-band);color:rgba(255,255,255,.72)}
.hs-band .section-tag{color:var(--c-vert-lt)}
.hs-band .section-tag::before{background:var(--c-vert-lt)}
.hs-h2{font-family:var(--ff-h);font-size:clamp(30px,4.4vw,54px);font-weight:800;letter-spacing:-.045em;line-height:1.05;color:var(--c-ink);margin:0 0 20px;max-width:760px;text-wrap:balance}
.hs-band .hs-h2{color:#fff}
.hs-lead{font-size:17px;font-weight:300;color:var(--c-mid);line-height:1.8;max-width:620px;margin:0 0 52px;text-wrap:pretty}
.hs-band .hs-lead{color:rgba(255,255,255,.68)}
/* Bouton principal : base complète (certaines pages n'ont pas le CSS de l'accueil) */
.btn-primary{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-family:var(--ff-h);font-size:15px;font-weight:700;letter-spacing:-.02em;padding:14px 28px;border-radius:999px;border:none;text-decoration:none;cursor:pointer;background:var(--c-vert-lt);color:#0a0a09;transition:background .2s,transform .18s,box-shadow .2s}
.btn-primary:hover{transform:translateY(-2px)}
/* Hero */
.hs-hero{position:relative;overflow:hidden;background:var(--c-bg);padding:calc(var(--topbar-h,40px) + 120px) 0 104px}
.hs-hero-deco{position:absolute;inset:0;pointer-events:none;background:radial-gradient(circle at 50% 0%,rgba(0,194,126,.08) 0,transparent 46%),radial-gradient(circle at 100% 100%,rgba(0,194,126,.06) 0,transparent 34%)}
.hs-hero-deco::after{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(0,0,0,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.03) 1px,transparent 1px);background-size:72px 72px;-webkit-mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,#000 0,transparent 100%);mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,#000 0,transparent 100%)}
html[data-theme="dark"] .hs-hero-deco::after{background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px)}
.hs-hero-grid{position:relative;display:grid;grid-template-columns:minmax(0,1fr);gap:64px;align-items:center}
.hs-hero.has-card .hs-hero-grid{grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr)}
.hs-hero .breadcrumb{font-size:13px;color:var(--c-muted);margin:0 0 22px}
.hs-hero .breadcrumb a{color:var(--c-muted);text-decoration:none}
.hs-hero .breadcrumb a:hover{color:var(--c-vert-txt)}
.hs-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 14px 5px 8px;background:var(--c-vert-bg);border:1px solid var(--c-vert-br);border-radius:999px;font-size:12.5px;font-weight:500;color:var(--c-vert-txt);margin:0 0 26px}
.hs-badge .badge-dot{width:6px;height:6px;border-radius:50%;background:var(--c-vert);flex-shrink:0}
.hs-hero h1{font-family:var(--ff-h);font-size:clamp(38px,5.6vw,68px);font-weight:800;letter-spacing:-.05em;line-height:1.02;color:var(--c-ink);margin:0 0 26px;max-width:760px;text-wrap:balance}
.hs-hero h1 em{font-style:normal;color:var(--c-vert)}
.hs-hero.has-card h1{font-size:clamp(36px,4.5vw,58px)}
.hs-hero-lead{font-size:17px;font-weight:300;line-height:1.75;color:var(--c-mid);max-width:560px;margin:0;text-wrap:pretty}
.hs-ctas{display:flex;flex-wrap:wrap;gap:12px;margin:34px 0 0}
.hs-btn-ghost{display:inline-flex;align-items:center;gap:8px;font-family:var(--ff-h);font-size:15px;font-weight:600;letter-spacing:-.02em;color:var(--c-ink);padding:14px 28px;border-radius:999px;border:1px solid var(--c-border2);text-decoration:none;transition:border-color .2s}
.hs-btn-ghost:hover{border-color:var(--c-ink)}
.hs-mini{display:flex;flex-wrap:wrap;gap:8px 28px;margin:30px 0 0;font-size:13.5px;color:var(--c-mid)}
.hs-mini b{color:var(--c-vert-txt);font-weight:700;margin-right:4px}
/* Carte « recommandation » (hero de la home) */
.hs-reco{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:24px;padding:24px;box-shadow:0 28px 70px rgba(0,0,0,.09)}
.hs-reco-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 14px}
.hs-reco-head .t{font-family:var(--ff-h);font-weight:800;font-size:15px;color:var(--c-ink)}
.hs-reco-pill{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;background:var(--c-vert-bg);color:var(--c-vert-txt);padding:5px 11px;border-radius:999px;white-space:nowrap}
.hs-reco-row{display:flex;align-items:center;gap:14px;padding:13px 0;border-top:1px solid var(--c-border)}
.hs-reco-ico{width:42px;height:42px;border-radius:12px;background:var(--c-vert-bg);color:var(--c-vert);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hs-reco-row .k{font-size:12px;color:var(--c-muted)}
.hs-reco-row .v{font-family:var(--ff-h);font-weight:700;font-size:16px;color:var(--c-ink);letter-spacing:-.02em}
.hs-reco-row .r{margin-left:auto;text-align:right}
.hs-reco-foot{margin:16px 0 0;background:var(--c-band);color:#fff;border-radius:14px;padding:13px 15px;display:flex;align-items:center;gap:9px;font-size:12px;line-height:1.45}
.hs-reco-foot svg{color:var(--c-vert-lt);flex-shrink:0}
html[data-theme="dark"] .hs-reco-foot{border:1px solid var(--c-border2)}
/* Cartes à bord supérieur vert + tuile noire */
.hs-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:20px}
.hs-card-top{background:var(--c-bg2);border-radius:20px;border-top:4px solid var(--c-vert);padding:30px 26px;box-shadow:0 10px 32px rgba(0,0,0,.05)}
.hs-tile{width:54px;height:54px;border-radius:14px;background:#000;color:var(--c-vert-lt);display:flex;align-items:center;justify-content:center;margin:0 0 24px}
html[data-theme="dark"] .hs-tile{border:1px solid var(--c-border2)}
.hs-card-top h3,.hs-card-num h3{font-family:var(--ff-h);font-size:19px;font-weight:700;letter-spacing:-.03em;color:var(--c-ink);margin:0 0 10px;text-wrap:balance}
.hs-card-top h3,.hs-card-num h3{min-height:2.5em}
.hs-card-top .amt{display:block;font-family:var(--ff-h);font-size:26px;font-weight:800;letter-spacing:-.04em;color:var(--c-vert-txt);margin:0 0 10px}
.hs-card-top p,.hs-card-num p{font-size:14.5px;line-height:1.7;color:var(--c-mid);margin:0;text-wrap:pretty}
/* Cartes contour + gros numéro */
.hs-card-num{border:1.5px solid var(--c-border2);border-radius:20px;padding:30px 28px;transition:border-color .25s,transform .25s}
.hs-card-num:hover{border-color:var(--c-vert);transform:translateY(-4px)}
.hs-card-num .hd{display:flex;align-items:center;justify-content:space-between;margin:0 0 30px}
.hs-ico-o{width:50px;height:50px;border-radius:14px;border:1.6px solid var(--c-vert);color:var(--c-vert);display:flex;align-items:center;justify-content:center}
.hs-num{font-family:var(--ff-h);font-size:38px;font-weight:800;letter-spacing:-.04em;color:rgba(0,194,126,.22);line-height:1}
/* Étapes sur bande noire */
.hs-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:20px}
.hs-step{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:32px 24px;transition:background .2s,transform .25s}
.hs-step:hover{background:rgba(255,255,255,.08);transform:translateY(-4px)}
.hs-pill{display:inline-flex;font-family:var(--ff-h);font-size:12px;font-weight:800;letter-spacing:-.01em;background:var(--c-vert);color:#05231a;padding:7px 12px;border-radius:8px;margin:0 0 22px}
.hs-step h3{font-family:var(--ff-h);font-size:17px;font-weight:700;letter-spacing:-.03em;color:#fff;margin:0 0 10px;text-wrap:balance}
.hs-step p{font-size:14px;line-height:1.7;color:rgba(255,255,255,.68);margin:0;text-wrap:pretty}
.hs-note{display:flex;align-items:center;gap:10px;margin:32px 0 0;font-size:14.5px;color:rgba(255,255,255,.75)}
.hs-note svg{color:var(--c-vert-lt);flex-shrink:0}
.hs-note b{color:#fff}
/* Bande de chiffres */
.hs-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.hs-stat{text-align:center;padding:8px 28px;border-left:1px solid rgba(255,255,255,.12)}
.hs-stat:first-child{border-left:none}
.hs-stat .n{display:block;font-family:var(--ff-h);font-size:clamp(40px,4.4vw,56px);font-weight:800;letter-spacing:-.05em;line-height:1;color:var(--c-vert-lt);margin:0 0 12px}
.hs-stat p{font-size:14px;line-height:1.6;color:rgba(255,255,255,.7);margin:0 auto;max-width:240px;text-wrap:balance}
/* 2 colonnes texte / encadré */
.hs-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:56px;align-items:start}
.hs-prose p{font-size:16.5px;line-height:1.85;color:var(--c-mid);margin:0 0 18px;text-wrap:pretty}
.hs-box{background:var(--c-bg);border:1px solid var(--c-border);border-radius:20px;padding:28px}
.hs-white .hs-box{background:var(--c-bg)}
.hs-menthe .hs-box{background:var(--c-bg2)}
.hs-box h3{font-family:var(--ff-h);font-size:17px;font-weight:700;letter-spacing:-.025em;color:var(--c-ink);margin:0 0 12px;display:flex;align-items:center;gap:10px}
.hs-box h3 svg{color:var(--c-vert)}
.hs-box p{font-size:14.5px;line-height:1.75;color:var(--c-mid);margin:0}
.hs-box-dark{background:var(--c-band)!important;border-color:transparent;margin-top:16px}
.hs-box-dark h3{color:#fff}
.hs-box-dark p{color:rgba(255,255,255,.7);margin:0 0 20px}
/* FAQ 2 colonnes */
.hs-faq-grid{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:56px;align-items:start}
.hs-faq-grid .hs-lead{margin-bottom:0}
.hs-faq-grid .hs-h2{font-size:clamp(28px,3.2vw,40px)}
.hs-faq-grid .faq-city{margin:0}
.faq-city summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px}
.faq-city summary::-webkit-details-marker{display:none}
.hs-sec a.pt-inline{color:var(--c-vert-txt);text-decoration:underline;text-underline-offset:3px}
.faq-city details>p{margin:0;padding:0 24px 20px;font-size:15px;line-height:1.8;color:var(--c-mid)}
.hs-sec .pt-note{margin-top:28px}
/* CTA final */
.hs-cta{background:var(--c-band);border-radius:28px;padding:64px 48px;text-align:center}
.hs-cta h2{font-family:var(--ff-h);font-size:clamp(26px,3.4vw,40px);font-weight:800;letter-spacing:-.04em;line-height:1.1;color:#fff;margin:0 auto 14px;max-width:640px;text-wrap:balance}
.hs-cta p{font-size:16px;line-height:1.7;color:rgba(255,255,255,.68);margin:0 auto 30px;max-width:520px;text-wrap:pretty}
html[data-theme="dark"] .hs-cta{border:1px solid var(--c-border2)}
.hs-pills{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 40px}
.hs-pills .rl{font-size:14px;color:var(--c-mid);margin-right:4px}
.hs-pills a{display:inline-flex;padding:9px 18px;border-radius:999px;background:var(--c-bg2);border:1px solid var(--c-border);color:var(--c-ink);font-family:var(--ff-h);font-weight:700;font-size:14px;text-decoration:none;transition:border-color .2s,color .2s}
.hs-pills a:hover{border-color:var(--c-vert-br);color:var(--c-vert-txt)}
@media(max-width:900px){
  .hs-hero.has-card .hs-hero-grid,.hs-split,.hs-faq-grid{grid-template-columns:minmax(0,1fr);gap:40px}
  .hs-stats{grid-template-columns:minmax(0,1fr)}
  .hs-stat{border-left:none;border-top:1px solid rgba(255,255,255,.12);padding:24px 0}
  .hs-stat:first-child{border-top:none}
}
@media(max-width:640px){
  .hs-sec{padding:72px 0}
  .hs-wrap{padding:0 20px}
  .hs-hero{padding:calc(var(--topbar-h,40px) + 100px) 0 72px}
  .hs-hero h1{font-size:clamp(34px,10vw,44px)}
  .hs-lead{margin-bottom:36px}
  .hs-cta{padding:44px 24px;border-radius:22px}
  .hs-ctas a{width:100%;justify-content:center}
  .hs-reco{padding:18px}
}
</style>'''
