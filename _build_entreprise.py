#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère la landing page /entreprise.html (entreprises & flottes : SEO + formulaire dédié).
Sources des faits : blog/borne-recharge-entreprise-loi-lom-2026.html (ne rien inventer)."""
import json
from _build_villes import (GA, FAVICON, FONTS, CSS, EXTRA_CSS, UNIFORM, PRELOADER,
                           NAVLOGO, ARROW, footer)

URL = "https://leseclaires.fr/entreprise"
DESC = ("Bornes de recharge en entreprise et pour les flottes : obligations loi LOM, "
        "dimensionnement, pilotage de charge, aides 2026 et TVA récupérable. "
        "Mise en relation gratuite avec un installateur certifié IRVE.")

FORM_CSS = '''<style>
.copro-form{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-xl);padding:36px;margin-bottom:48px}
.copro-form .row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
.copro-legal{font-size:12.5px;line-height:1.6;color:var(--c-muted);margin:4px 0 18px}
.copro-legal a{color:var(--c-vert-txt);text-decoration:underline}
.copro-form label{display:block;font-size:13px;font-weight:600;color:var(--c-mid);margin-bottom:6px}
.copro-form input,.copro-form select,.copro-form textarea{width:100%;background:var(--c-bg);border:1px solid var(--c-border2);border-radius:var(--r-sm);padding:13px 15px;font-size:15px;font-family:var(--ff-b);color:var(--c-text);outline:none;box-sizing:border-box;transition:border-color .2s,box-shadow .2s}
.copro-form input:focus,.copro-form select:focus,.copro-form textarea:focus{border-color:rgba(0,194,126,.5);box-shadow:0 0 0 3px rgba(0,194,126,.1)}
.copro-form textarea{min-height:110px;resize:vertical}
.copro-form .full{grid-column:1/-1}
.copro-form .btn-vert{border:none;cursor:pointer;margin-top:4px}
.copro-ok{display:none;text-align:center;padding:24px;background:var(--c-vert-bg);border:1px solid var(--c-vert-br);border-radius:var(--r-lg)}
.copro-ok.show{display:block}
.copro-ok h4{font-family:var(--ff-h);font-size:18px;color:var(--c-ink);margin:0 0 6px}
.copro-ok p{margin:0;color:var(--c-mid)}
@media(max-width:560px){.copro-form .row{grid-template-columns:1fr}}
.hs-prose a,.hs-box a:not(.btn-primary),.hs-lead a{color:var(--c-vert-txt);text-decoration:underline;text-underline-offset:2px}
</style>'''

FAQ = [
 ("Mon entreprise est-elle obligée d'installer des bornes de recharge ?",
  "Pas toutes. La loi LOM vise les bâtiments non résidentiels (bureaux, commerces, industrie, ERP) dotés d'un parking de plus de 20 places : depuis le 1er janvier 2025, ils doivent disposer d'un point de recharge par tranche de 20 places, dont un accessible aux personnes à mobilité réduite. Les constructions neuves et les rénovations importantes ont des obligations renforcées. Un audit sur site détermine votre obligation réelle."),
 ("Combien coûte l'installation de bornes en entreprise ?",
  "Comptez à partir d'environ 1&nbsp;200 à 2&nbsp;000&nbsp;€&nbsp;TTC par borne 7,4&nbsp;kW. Le coût par point de charge baisse fortement dès que l'on équipe plusieurs places, grâce à une infrastructure mutualisée et au pilotage de charge."),
 ("Quelles aides pour une borne de recharge en entreprise ?",
  "En 2026, la prime ADVENIR ne finance plus les bornes installées sur un parking privé d'entreprise pour les salariés ou une flotte de véhicules légers. Elle reste ouverte pour l'habitat collectif, la voirie publique et les poids lourds. Pour une entreprise assujettie à la TVA, la TVA sur l'investissement est récupérable, et le matériel est amortissable. Le crédit d'impôt des particuliers ne concerne pas les sociétés."),
 ("À quoi sert le pilotage de charge ?",
  "Il répartit la puissance électrique disponible entre les véhicules en charge. Sans lui, équiper plusieurs places obligerait à augmenter fortement la puissance souscrite, donc l'abonnement. Avec lui, on équipe davantage de places sur la même alimentation."),
 ("Peut-on refacturer la recharge aux salariés ou aux visiteurs ?",
  "Oui. Une solution de supervision mesure la consommation de chaque borne et permet de refacturer l'électricité selon la politique de l'entreprise. C'est un point à cadrer dès la conception du projet."),
 ("Faut-il un installateur certifié IRVE ?",
  "Oui. La qualification IRVE est obligatoire au-delà de 3,7&nbsp;kW. Elle doit figurer sur le devis comme sur la facture. Nous vous mettons en relation avec un installateur certifié IRVE."),
]
faq_html = '\n'.join(f'    <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q,a in FAQ)
import re as _re
faq_ld = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":_re.sub('&nbsp;',' ',a)}} for q,a in FAQ]

graph = {"@context":"https://schema.org","@graph":[
  {"@type":"Service","name":"Bornes de recharge pour entreprises et flottes","description":DESC,
   "provider":{"@type":"Organization","name":"Les Éclairés","url":"https://leseclaires.fr"},
   "areaServed":{"@type":"Country","name":"France"},"url":URL},
  {"@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Accueil","item":"https://leseclaires.fr/"},
    {"@type":"ListItem","position":2,"name":"Entreprise et flotte","item":URL}]},
  {"@type":"FAQPage","mainEntity":faq_ld},
]}
jsonld='<script type="application/ld+json">\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n</script>'

import _home_sections as hs
_card = hs.reco_card("Votre projet entreprise", "Gratuit",
    [("scale", "Loi LOM (parking de plus de 20 places)", "1 point / 20 places", "Depuis le", "1er&nbsp;janv. 2025"),
     ("percent", "TVA sur l'investissement", "Récupérable*", "Matériel", "Amortissable"),
     ("users", "Mise en relation", "1 installateur", "Qualification", "Certifié IRVE")],
    'Réponse <b style="color:var(--c-vert-lt)">sous 24 à 48&nbsp;h</b> · *si votre entreprise est assujettie')
body = hs.hero(crumbs='<a href="/">Accueil</a> › <span>Entreprise et flotte</span>',
    badge="Entreprises, commerces &amp; flottes · Service gratuit",
    h1="Des bornes de recharge <em>pour votre entreprise</em>",
    lead="Parking salariés, visiteurs ou véhicules de société : on vous aide à comprendre vos obligations (loi LOM), à dimensionner une infrastructure qui suivra l'électrification de votre flotte, et on vous met en relation avec un installateur certifié IRVE habitué aux sites professionnels.",
    ctas=[("#contact-entreprise", "Parler de mon projet", "primary"), ("#obligations", "Mes obligations", "ghost")],
    mini=[("20&nbsp;places", "seuil loi LOM"), ("24-48&nbsp;h", "pour une réponse"), ("100&nbsp;%", "indépendant")],
    card=_card)
body += hs.section(hs.top_cards([
    ("bolt", "Dimensionner juste", "", "Combien de véhicules aujourd'hui, combien demain&nbsp;? On équipe pour la trajectoire de votre flotte, pas seulement pour l'instant présent."),
    ("clock", "Pilotage de charge", "", "La puissance disponible est répartie entre les véhicules&nbsp;: plus de places équipées sans exploser l'abonnement électrique."),
    ("euro", "Un coût net maîtrisé", "", "TVA récupérable pour les entreprises assujetties et matériel amortissable&nbsp;: le coût réel est inférieur au montant du devis."),
    ("building", "Infrastructure évolutive", "", "Une alimentation mutualisée posée une fois&nbsp;: les bornes suivantes s'ajoutent sans rouvrir le parking."),
  ]), tone='menthe', tag="Ce qui compte", h2="Les 4 clés d'un projet entreprise réussi",
  lead="Le poste le plus stratégique n'est pas la borne, c'est l'infrastructure et le pilotage de charge. C'est là que se jouent le budget et l'évolutivité.")
body += hs.section('<div class="hs-split"><div class="hs-prose"><p>' + "La loi d'orientation des mobilités (LOM) impose aux bâtiments non résidentiels dotés d'un parking de plus de 20 places un point de recharge par tranche de 20 places (dont un accessible aux personnes à mobilité réduite) depuis le 1er janvier 2025. Les bâtiments neufs ou en rénovation importante (parking de plus de 10 places) doivent pré-équiper une part significative des places, et les grands parkings (plus de 200 places) ont des obligations renforcées." + '</p><p>' + "Les seuils exacts dépendent de la taille du parking et de la date de construction. Un audit sur site évite à la fois la sous-conformité et le surdimensionnement." + ' <a href="/blog/borne-recharge-entreprise-loi-lom-2026.html">Le détail de la loi LOM en 2026</a>.</p></div><div>'
  + '<div class="hs-box"><h3>' + hs.icon("percent", 20) + 'Prime ADVENIR&nbsp;: plus pour les parkings d\'entreprise</h3><p>Depuis 2026, ADVENIR ne finance plus les bornes réservées aux salariés ou aux flottes de véhicules légers sur parking privé. Elle reste ouverte pour l\'habitat collectif, la voirie publique et les poids lourds (<a href="https://advenir.mobi/" target="_blank" rel="noopener">advenir.mobi</a>).</p></div>'
  + '<div class="hs-box hs-box-dark"><h3>Pas sûr de votre obligation&nbsp;?</h3><p>Décrivez votre site, on vous oriente et on vous met en relation avec un installateur qui réalisera l\'audit.</p><a href="#contact-entreprise" class="btn-primary">Parler de mon projet ' + hs.ARROW + '</a></div>'
  + '</div></div>', tone='white', tag="Le cadre légal", h2="Loi LOM&nbsp;: ce que votre entreprise doit savoir", sid="obligations")
body += hs.section(hs.steps([
    ("Vous décrivez votre site", "Nombre de places, véhicules de la flotte, usage (salariés, visiteurs, véhicules de service), échéance."),
    ("On vous oriente", "Obligations probables, ordre de grandeur du budget, aides mobilisables et points à vérifier."),
    ("Mise en relation", "Avec un installateur certifié IRVE habitué aux sites professionnels, qui réalise l'audit et le devis."),
    ("Installation &amp; supervision", "Bornes, pilotage de charge et, si besoin, supervision pour suivre et refacturer la recharge."),
  ]), tone='band', tag="Comment ça se passe", h2="Votre projet entreprise en 4 étapes")
import _form_shared as fs
_FORM_ROWS = [
    [fs.field('cNom','Nom et prénom',placeholder='Votre nom',autocomplete='name'), fs.field('cSoc','Entreprise',placeholder='Raison sociale',autocomplete='organization')],
    [fs.field('cCP','Code postal du site',placeholder='69003',autocomplete='postal-code',inputmode='numeric',extra=' maxlength="5"'), fs.field('cPlaces','Places de parking',options=['Moins de 10','10 à 20','21 à 50','51 à 200','Plus de 200'])],
    [fs.field('cEmail','Email',kind='email',placeholder='vous@entreprise.fr',autocomplete='email'), fs.field('cTel','Téléphone',kind='tel',placeholder='06 12 34 56 78',autocomplete='tel',inputmode='tel')],
    [fs.field('cUsage','Usage principal',options=['Flotte de véhicules de société','Salariés','Clients / visiteurs','Plusieurs usages'])],
    [fs.field('cMsg','Votre projet (facultatif)',kind='textarea',placeholder='Nombre de bornes envisagées, véhicules, échéance…')],
  ]
body += hs.section(fs.form_html(_FORM_ROWS, 'En envoyant, vous acceptez que ces informations soient transmises à un seul installateur certifié IRVE partenaire, habitué aux sites professionnels, qui vous recontactera. Service gratuit&nbsp;: Les Éclairés est rémunéré par l\'installateur. <a href="/confidentialite.html">Confidentialité</a> · <a href="/cgu.html">Conditions d\'utilisation</a>.', ARROW), tone='menthe', tag="Parlons de votre site", h2="Être mis en relation gratuitement",
  lead="Décrivez votre site en quelques lignes. On revient vers vous sous 24 à 48 heures, sans engagement. Particulier&nbsp;? Utilisez plutôt <a href=\"/simulateur\">le simulateur</a>.", sid="contact-entreprise")
body += hs.faq_section("Questions fréquentes", "Bornes en entreprise&nbsp;: vos questions",
  "Les réponses aux questions que se posent dirigeants, services généraux et gestionnaires de flotte.", faq_html)

# Le formulaire est une chaîne non formatée : on y injecte la flèche ici
body = body.replace('{ARROW}', ARROW)

FORM_JS = fs.form_js(title='NOUVEAU LEAD - Entreprise / Flotte', subject='Lead entreprise', from_name='Entreprise Les Éclairés', segment='Entreprise', lines=[['Nom','cNom'],['Entreprise','cSoc'],['Code postal','cCP'],['Places de parking','cPlaces'],['Usage','cUsage'],['Email','cEmail'],['Téléphone','cTel'],['Projet','cMsg']])

html=f'''<!DOCTYPE html>
<html lang="fr">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Borne de recharge entreprise &amp; flotte : loi LOM, aides | Les Éclairés</title>
<meta name="description" content="{DESC}">
<meta name="keywords" content="borne recharge entreprise, borne recharge flotte, IRVE entreprise, loi LOM borne parking, pilotage de charge">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Bornes de recharge pour entreprises et flottes | Les Éclairés">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://leseclaires.fr/nous-les-eclaires.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bornes de recharge pour entreprises et flottes | Les Éclairés">
<meta name="twitter:description" content="{DESC}">
{FAVICON}
{FONTS}
{jsonld}
{CSS}
{EXTRA_CSS}
{FORM_CSS}
{fs.CSS}
{UNIFORM}
<noscript><style>#preloader{{display:none!important}}</style></noscript>
</head>
<body>
{PRELOADER}
<nav>
  <a class="nav-logo" href="/"><img src="{NAVLOGO}" alt="Les Éclairés"><span>Les Éclairés</span></a>
  <a class="btn-nav" href="#contact-entreprise">Parler de mon projet</a>
</nav>

{body}
{footer()}
  <script src="/cursor.js" defer></script>
{FORM_JS}
</body>
</html>
'''
open('entreprise.html','w',encoding='utf-8').write(html)
print("entreprise.html écrit :", len(html), "octets")

# Topbar partenaire + bulle cookie (durable après rebuild)
import _inject_header
_inject_header.inject_file('entreprise.html', is_blog=False)
# Mode sombre (durable après rebuild)
import _apply_dark
_apply_dark.apply('entreprise.html')
import _legal_global
_legal_global.apply('entreprise.html')
