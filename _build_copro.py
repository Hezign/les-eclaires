#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère la landing page /copropriete.html (SEO + formulaire de contact dédié)."""
import json
from _build_villes import (GA, FAVICON, FONTS, CSS, EXTRA_CSS, UNIFORM, PRELOADER,
                           NAVLOGO, ARROW, footer)

URL = "https://leseclaires.fr/copropriete"
DESC = ("Bornes de recharge en copropriété : droit à la prise, prime ADVENIR, "
        "infrastructure collective. On accompagne syndics et conseils syndicaux de A à Z. "
        "Étude gratuite et sans engagement.")

FORM_CSS = '''<style>
.copro-form{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-xl);padding:36px;margin-bottom:48px}
.copro-form .row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.copro-form label{display:block;font-size:13px;font-weight:600;color:var(--c-mid);margin-bottom:6px}
.copro-form input,.copro-form select,.copro-form textarea{width:100%;background:var(--c-bg);border:1px solid var(--c-border2);border-radius:var(--r-sm);padding:13px 15px;font-size:15px;font-family:var(--ff-b);color:var(--c-text);outline:none;box-sizing:border-box;transition:border-color .2s,box-shadow .2s}
.copro-form input:focus,.copro-form select:focus,.copro-form textarea:focus{border-color:rgba(0,169,110,.5);box-shadow:0 0 0 3px rgba(0,169,110,.1)}
.copro-form textarea{min-height:110px;resize:vertical}
.copro-form .full{grid-column:1/-1}
.copro-form .btn-vert{border:none;cursor:pointer;margin-top:4px}
.copro-ok{display:none;text-align:center;padding:24px;background:var(--c-vert-bg);border:1px solid var(--c-vert-br);border-radius:var(--r-lg)}
.copro-ok.show{display:block}
.copro-ok h4{font-family:var(--ff-h);font-size:18px;color:var(--c-ink);margin:0 0 6px}
.copro-ok p{margin:0;color:var(--c-mid)}
@media(max-width:560px){.copro-form .row{grid-template-columns:1fr}}
</style>'''

FAQ = [
 ("Qui peut lancer un projet de bornes en copropriété ?",
  "N'importe quel copropriétaire peut demander l'installation d'une borne pour son usage (droit à la prise). Pour un projet collectif couvrant tout le parking, c'est le conseil syndical et le syndic qui pilotent, après un vote en assemblée générale."),
 ("Qu'est-ce que le droit à la prise ?",
  "Le droit à la prise permet à tout occupant (propriétaire ou locataire) d'installer à ses frais une borne sur sa place de stationnement, sans avoir besoin de l'accord de l'assemblée générale. Le syndic ne peut s'y opposer que pour un motif sérieux et légitime."),
 ("Combien coûte l'installation de bornes en copropriété ?",
  "Cela dépend du nombre de points de charge et de l'infrastructure à poser. Le coût par borne baisse fortement quand on équipe plusieurs places en même temps, surtout en posant une infrastructure collective évolutive. La prime ADVENIR réduit nettement la facture."),
 ("Qu'est-ce que la prime ADVENIR en copropriété ?",
  "ADVENIR est une aide qui finance l'installation de bornes en copropriété : jusqu'à 960 € par point de charge, et une part importante de l'infrastructure collective. La demande doit être faite avant le début des travaux."),
 ("Faut-il un vote en assemblée générale ?",
  "Pour une installation individuelle au titre du droit à la prise, non. Pour une infrastructure collective (qui équipe l'ensemble du parking), oui : le projet est inscrit à l'ordre du jour et voté en assemblée générale."),
 ("Combien de temps prend un projet en copropriété ?",
  "Comptez généralement de quelques semaines à quelques mois selon la taille de la copropriété et le calendrier des assemblées générales. On vous aide à cadrer le projet pour éviter les allers-retours."),
]
faq_html = '\n'.join(f'    <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q,a in FAQ)
faq_ld = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]

graph = {"@context":"https://schema.org","@graph":[
  {"@type":"Service","name":"Installation de bornes de recharge en copropriété","description":DESC,
   "provider":{"@type":"Organization","name":"Les Éclairés","url":"https://leseclaires.fr"},
   "areaServed":{"@type":"Country","name":"France"},"url":URL},
  {"@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Accueil","item":"https://leseclaires.fr/"},
    {"@type":"ListItem","position":2,"name":"Copropriété","item":URL}]},
  {"@type":"FAQPage","mainEntity":faq_ld},
]}
jsonld='<script type="application/ld+json">\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n</script>'

html=f'''<!DOCTYPE html>
<html lang="fr">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bornes de recharge en copropriété : guide syndics &amp; copropriétaires | Les Éclairés</title>
<meta name="description" content="{DESC}">
<meta name="keywords" content="borne recharge copropriété, IRVE copropriété, droit à la prise, prime ADVENIR copropriété, borne syndic, infrastructure recharge collective">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Bornes de recharge en copropriété | Les Éclairés">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://leseclaires.fr/nous-les-eclaires.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bornes de recharge en copropriété | Les Éclairés">
<meta name="twitter:description" content="{DESC}">
{FAVICON}
{FONTS}
{jsonld}
{CSS}
{EXTRA_CSS}
{FORM_CSS}
{UNIFORM}
<noscript><style>#preloader{{display:none!important}}</style></noscript>
</head>
<body>
{PRELOADER}
<nav>
  <a class="nav-logo" href="/"><img src="{NAVLOGO}" alt="Les Éclairés"><span>Les Éclairés</span></a>
  <a class="btn-nav" href="#contact-copro">Étudier mon projet</a>
</nav>

<div class="hero-city">
  <div class="breadcrumb"><a href="/">Accueil</a> › <span>Copropriété</span></div>
  <div class="city-badge"><span class="badge-dot"></span>Syndics &amp; conseils syndicaux · Étude gratuite</div>
  <h1 class="city-h1">Des bornes de recharge<br><span style="white-space:nowrap">pour votre copropriété</span></h1>
  <p class="city-sub">Équiper une copropriété en bornes de recharge, c'est anticiper la demande des résidents et valoriser l'immeuble - souvent plusieurs dizaines de points de charge. On accompagne les syndics et les conseils syndicaux de A à Z : droit à la prise, prime ADVENIR, infrastructure collective évolutive.</p>
  <a href="#contact-copro" class="btn-primary">Étudier mon projet copropriété {ARROW}</a>
</div>

<div class="city-body">

  <span class="section-tag">Pourquoi maintenant</span>
  <h2 class="section-h2">Pourquoi équiper votre copropriété</h2>
  <p class="section-lead">La demande de recharge explose, et le cadre légal pousse les copropriétés à s'équiper. Anticiper, c'est éviter l'urgence et les surcoûts.</p>
  <div class="info-grid">
    <div class="info-card"><h4>Valorisation des lots</h4><p>Une place équipée (ou pré-équipée) d'une borne devient un vrai argument à la vente comme à la location.</p></div>
    <div class="info-card"><h4>Une infrastructure mutualisée</h4><p>On pose une fois une colonne montante évolutive : chaque résident peut ensuite se raccorder à moindre coût.</p></div>
    <div class="info-card"><h4>Jusqu'à 960 € / point</h4><p>La prime ADVENIR finance une part importante des points de charge et de l'infrastructure collective.</p></div>
    <div class="info-card"><h4>Un seul interlocuteur</h4><p>On cadre le projet, on mobilise un installateur certifié IRVE et on vous accompagne jusqu'au vote en AG.</p></div>
  </div>

  <span class="section-tag">Le cadre légal</span>
  <h2 class="section-h2">Droit à la prise &amp; prime ADVENIR</h2>
  <p class="section-lead">Deux leviers majeurs facilitent l'installation de bornes en copropriété.</p>
  <div class="areas-section">
    <h4>Le droit à la prise</h4>
    <p>Tout copropriétaire ou locataire peut faire installer une borne sur sa place de parking, à ses frais, sans accord préalable de l'assemblée générale. Le syndic ne peut s'y opposer que pour un motif sérieux et légitime. Pour un projet collectif couvrant tout le parking, un vote en AG est en revanche nécessaire - on vous aide à le préparer.</p>
  </div>

  <span class="section-tag">Comment ça se passe</span>
  <h2 class="section-h2">Votre projet copropriété en 4 étapes</h2>
  <div class="info-grid">
    <div class="info-card"><h4>1. Vous nous décrivez la copro</h4><p>Nombre de lots, type de parking, année de construction, projet individuel ou collectif.</p></div>
    <div class="info-card"><h4>2. On cadre le projet</h4><p>On définit l'infrastructure adaptée, le budget, les aides mobilisables et le déroulé jusqu'à l'AG.</p></div>
    <div class="info-card"><h4>3. Mise en relation</h4><p>On vous met en relation avec un installateur certifié IRVE habitué aux copropriétés de votre taille.</p></div>
    <div class="info-card"><h4>4. Installation</h4><p>L'infrastructure est posée ; chaque résident peut ensuite se raccorder simplement, au fil de ses besoins.</p></div>
  </div>

  <span class="section-tag" id="contact-copro">Parlons de votre copropriété</span>
  <h2 class="section-h2">Demander une étude gratuite</h2>
  <p class="section-lead">Décrivez votre copropriété en quelques lignes. On revient vers vous sous 24 à 48 heures, sans engagement.</p>
  <div class="copro-form">
    <div id="cBox">
      <div class="row">
        <div><label for="cNom">Nom et prénom</label><input type="text" id="cNom" placeholder="Votre nom"></div>
        <div><label for="cRole">Vous êtes</label><select id="cRole"><option value="" disabled selected>Sélectionnez…</option><option>Syndic professionnel</option><option>Syndic bénévole</option><option>Membre du conseil syndical</option><option>Copropriétaire</option><option>Autre</option></select></div>
      </div>
      <div class="row">
        <div><label for="cCopro">Nom / adresse de la copropriété</label><input type="text" id="cCopro" placeholder="Résidence, ville"></div>
        <div><label for="cLots">Nombre de lots</label><select id="cLots"><option value="" disabled selected>Sélectionnez…</option><option>Moins de 20</option><option>20 à 50</option><option>50 à 100</option><option>Plus de 100</option></select></div>
      </div>
      <div class="row">
        <div><label for="cEmail">Email</label><input type="email" id="cEmail" placeholder="vous@exemple.fr"></div>
        <div><label for="cTel">Téléphone</label><input type="tel" id="cTel" placeholder="06…"></div>
      </div>
      <div class="row"><div class="full"><label for="cMsg">Votre projet (facultatif)</label><textarea id="cMsg" placeholder="Type de parking, nombre de places à équiper, échéance…"></textarea></div></div>
      <button class="btn-vert" id="cSubmit" type="button">Envoyer ma demande {ARROW}</button>
    </div>
    <div class="copro-ok" id="cOk"><h4>Demande bien reçue !</h4><p>On revient vers vous sous 24 à 48 heures ouvrées.</p></div>
  </div>

  <span class="section-tag">Questions fréquentes</span>
  <h2 class="section-h2">Bornes en copropriété : vos questions</h2>
  <div class="faq-city">
{faq_html}
  </div>

</div>

{footer()}
  <script src="/cursor.js" defer></script>
<script>
(function(){{
  var KEY='1109c206-cadd-4010-a0c1-cf832975b2fa';
  function g(id){{return document.getElementById(id);}}
  function v(id){{var e=g(id);return e?(e.value||'').trim():'';}}
  var b=g('cSubmit'); if(!b) return; var sent=false;
  b.addEventListener('click', async function(){{
    var nom=v('cNom'), email=v('cEmail');
    if(!nom){{g('cNom').style.borderColor='rgba(220,50,50,.5)';return;}}
    if(!email){{g('cEmail').style.borderColor='rgba(220,50,50,.5)';return;}}
    if(sent) return; sent=true; b.textContent='Envoi…'; b.disabled=true;
    var msg='NOUVEAU LEAD - Copropriété\\n\\n'+
      'Nom : '+nom+'\\nRôle : '+(v('cRole')||'(non précisé)')+'\\n'+
      'Copropriété : '+(v('cCopro')||'(non précisé)')+'\\nNombre de lots : '+(v('cLots')||'(non précisé)')+'\\n'+
      'Email : '+email+'\\nTéléphone : '+(v('cTel')||'(non renseigné)')+'\\n\\nProjet : '+(v('cMsg')||'(non précisé)');
    try{{
      var r=await fetch('https://api.web3forms.com/submit',{{method:'POST',
        headers:{{'Content-Type':'application/json',Accept:'application/json'}},
        body:JSON.stringify({{access_key:KEY,subject:'Lead copropriété - '+nom,from_name:'Copropriété Les Éclairés',
          name:nom,email:email,replyto:email,message:msg}})}});
      var d=await r.json();
      if(d&&d.success){{g('cBox').style.display='none';g('cOk').classList.add('show');}}
      else throw new Error('w3f');
    }}catch(e){{sent=false;b.disabled=false;b.textContent='Envoyer ma demande';
      alert("Une erreur est survenue. Réessayez ou écrivez-nous à contact@leseclaires.fr.");}}
  }});
}})();
</script>
</body>
</html>
'''
open('copropriete.html','w',encoding='utf-8').write(html)
print("copropriete.html écrit :", len(html), "octets")
