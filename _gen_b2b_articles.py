#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère 2 articles B2B (cible installateurs = partenaires payants du modèle) :
  1. Devenir installateur agréé ADVENIR : conditions et démarches
  2. Quel logiciel de gestion pour installateur IRVE
Conforme blog/REDACTION.md : template, SEO block (BlogPosting+BreadcrumbList+FAQPage),
H2 en questions, réponse autoportante, ctamid, maillage, enregistrement
(accueil + listing + sitemap). Faits vérifiés (Qualifelec/AFNOR, Avere-France/CEE,
barème ADVENIR 01/04/2026, logiciels réels). Idempotent.
"""
import pathlib, re, json

ROOT = pathlib.Path(__file__).parent
BLOG = ROOT / "blog"
BASE = "https://leseclaires.fr"
TPL = (BLOG / "template.html").read_text(encoding="utf-8")

# ---------------------------------------------------------------- ARTICLE 1
A1_BODY = """
<p class="lead">Vous êtes électricien et vous voulez que vos clients profitent de la prime ADVENIR ? La bonne nouvelle : la clé n'est pas un agrément administratif obscur, c'est votre qualification IRVE. On vous explique ce qu'il faut réellement, et comment en faire un levier commercial.</p>

<h2 id="definition">Qu'est-ce qu'un installateur « agréé ADVENIR » ?</h2>
<p>Il n'existe pas d'agrément ADVENIR nominatif au sens strict. Ce qui rend un chantier éligible à la prime, c'est la <strong>qualification IRVE</strong> de l'installateur. ADVENIR est un programme national piloté par l'Avere-France et financé par les Certificats d'Économies d'Énergie (CEE), pas un label d'entreprise.</p>
<p>Concrètement, dès lors que vous êtes qualifié IRVE et que vous le mentionnez sur le devis puis la facture, vos clients (particuliers en copropriété, entreprises, syndics) peuvent monter un dossier ADVENIR. Se présenter comme « installateur ADVENIR », c'est donc d'abord afficher une qualification IRVE valide.</p>

<h2 id="conditions">Quelles conditions pour rendre vos chantiers éligibles ?</h2>
<p>Trois prérequis, tous liés au métier d'électricien, conditionnent l'éligibilité à ADVENIR.</p>
<ul>
  <li><strong>Être électricien qualifié et habilité</strong>, avec une expérience réelle des installations électriques.</li>
  <li><strong>Détenir une assurance responsabilité civile et décennale</strong> couvrant l'activité IRVE.</li>
  <li><strong>Être titulaire de la qualification IRVE</strong> (mention IRVE) délivrée par un organisme accrédité, et la faire figurer sur le devis <em>et</em> la facture.</li>
</ul>
<p>Sans la mention IRVE sur les documents, le dossier de prime est refusé, même si le travail est irréprochable. C'est le point de contrôle numéro un.</p>

<h2 id="qualification">Comment obtenir la qualification IRVE ?</h2>
<p>Deux organismes sont accrédités en France pour délivrer la qualification IRVE : <strong>Qualifelec</strong> et <strong>AFNOR Certification</strong>. La qualification passe par une formation dédiée et se décline en trois niveaux selon le type de chantier.</p>
<ul>
  <li><strong>Niveau 1 (P1)</strong> : bornes sans communication ni supervision, jusqu'à 22 kW. L'essentiel des installations résidentielles.</li>
  <li><strong>Niveau 2 (P2)</strong> : bornes communicantes et supervisées, configuration et pilotage à distance.</li>
  <li><strong>Niveau 3 (P3)</strong> : bornes en charge rapide en courant continu, puissances élevées.</li>
</ul>
<p>La qualification IRVE est obligatoire pour toute installation au-delà de 3,7 kW. C'est elle qui ouvre l'accès aux aides publiques pour vos clients, ADVENIR en tête.</p>

<div class="ctamid"><h3>Vous installez des bornes et cherchez des chantiers ?</h3><p>Les Éclairés orientent des particuliers et copropriétés vers des installateurs qualifiés IRVE.</p><a href="../partenaires.html">Rejoindre le réseau d'installateurs</a></div>

<h2 id="fonctionnement">Comment fonctionne une prime ADVENIR sur un chantier ?</h2>
<p>La règle d'or : le dossier ADVENIR doit être validé <strong>avant le début des travaux</strong>. Une demande déposée après coup est irrecevable. C'est souvent là que le client a besoin de vous.</p>
<ul>
  <li>Vous établissez un devis détaillé mentionnant la qualification IRVE et le taux de TVA applicable.</li>
  <li>Le bénéficiaire ou l'opérateur d'infrastructure dépose le dossier sur la plateforme ADVENIR, puis lance les travaux une fois la validation obtenue.</li>
  <li>La facture, elle aussi mention IRVE, sert de justificatif : la prime couvre 50 % des dépenses éligibles vérifiées, dans la limite des plafonds.</li>
</ul>
<p>Maîtriser ce séquencement fait de vous un interlocuteur de confiance, surtout en copropriété où le sujet du <a href="financement-infrastructure-collective-copropriete-advenir-2026.html">financement de l'infrastructure collective</a> est décisif au moment du vote en assemblée générale.</p>

<h2 id="baremes">Quels barèmes ADVENIR 2026 faut-il connaître ?</h2>
<p>Le barème en vigueur depuis le 1er avril 2026 en copropriété est le suivant (montants HT, prise en charge de 50 %).</p>
<table>
  <thead><tr><th>Type de projet</th><th>Aide maximale (HT)</th></tr></thead>
  <tbody>
    <tr><td>Borne individuelle en copropriété</td><td>Jusqu'à 1 000 EUR HT / point</td></tr>
    <tr><td>Borne partagée en copropriété</td><td>Jusqu'à 1 660 EUR HT / point</td></tr>
    <tr><td>Infrastructure collective (colonne électrique)</td><td>Jusqu'à 12 500 EUR HT (jusqu'à 100 places, + 125 EUR HT / place au-delà)</td></tr>
    <tr><td>Surprime travaux de voirie (VRD, parking extérieur)</td><td>Jusqu'à 8 000 EUR HT</td></tr>
    <tr><td>Surprime point de livraison dédié (bornes partagées)</td><td>Jusqu'à 3 000 EUR HT</td></tr>
  </tbody>
</table>
<p>Les pavillons individuels ne sont pas éligibles à ADVENIR : le programme vise les copropriétés et les bailleurs sociaux. Pour le détail complet des montants, voyez notre <a href="guide-prime-advenir-2026.html">guide de la prime ADVENIR 2026</a>.</p>

<h2 id="generer-chantiers">Comment générer plus de chantiers IRVE une fois qualifié ?</h2>
<p>La qualification ouvre la porte, mais ce sont vos canaux d'acquisition qui remplissent le carnet de commandes. Les leviers les plus efficaces en 2026 :</p>
<ul>
  <li><strong>Annuaires officiels</strong> : votre fiche sur qualifelec.fr et, le cas échéant, Qualit'EnR est consultée par les particuliers et les syndics.</li>
  <li><strong>Partenariats avec les syndics</strong> de copropriété, qui pilotent les projets d'infrastructure collective.</li>
  <li><strong>Appels d'offres des collectivités</strong> pour les bornes publiques et les flottes.</li>
  <li><strong>Plateformes de mise en relation</strong> qui qualifient la demande en amont et vous transmettent des projets prêts, comme le réseau Les Éclairés.</li>
</ul>
<p>Bien équipé, vous gagnez aussi du temps sur l'administratif : voyez notre comparatif du <a href="logiciel-gestion-installateur-irve.html">logiciel de gestion pour installateur IRVE</a>.</p>

<h2 id="faq">Questions fréquentes</h2>
<h3>Faut-il un agrément spécifique ADVENIR pour installer des bornes ?</h3>
<p>Non. Il n'y a pas d'agrément ADVENIR nominatif. C'est la qualification IRVE (Qualifelec ou AFNOR), mentionnée sur le devis et la facture, qui rend les travaux éligibles à la prime.</p>
<h3>Qui dépose le dossier ADVENIR, l'installateur ou le client ?</h3>
<p>Le dossier est déposé par le bénéficiaire ou l'opérateur d'infrastructure sur la plateforme ADVENIR, avant les travaux. L'installateur fournit un devis puis une facture conformes, avec la mention IRVE.</p>
<h3>La qualification IRVE est-elle obligatoire pour toutes les bornes ?</h3>
<p>Elle est obligatoire au-delà de 3,7 kW. En dessous, elle n'est pas exigée, mais elle reste indispensable pour que vos clients accèdent aux aides publiques.</p>
"""
A1_TOC = [("definition","Qu'est-ce qu'un installateur agréé ADVENIR ?"),
          ("conditions","Quelles conditions pour rendre vos chantiers éligibles ?"),
          ("qualification","Comment obtenir la qualification IRVE ?"),
          ("fonctionnement","Comment fonctionne une prime ADVENIR sur un chantier ?"),
          ("baremes","Quels barèmes ADVENIR 2026 faut-il connaître ?"),
          ("generer-chantiers","Comment générer plus de chantiers IRVE une fois qualifié ?"),
          ("faq","Questions fréquentes")]
A1_FAQ = [
 ("Faut-il un agrément spécifique ADVENIR pour installer des bornes ?",
  "Non. Il n'y a pas d'agrément ADVENIR nominatif. C'est la qualification IRVE (Qualifelec ou AFNOR), mentionnée sur le devis et la facture, qui rend les travaux éligibles à la prime."),
 ("Qui dépose le dossier ADVENIR, l'installateur ou le client ?",
  "Le dossier est déposé par le bénéficiaire ou l'opérateur d'infrastructure sur la plateforme ADVENIR, avant les travaux. L'installateur fournit un devis puis une facture conformes, avec la mention IRVE."),
 ("La qualification IRVE est-elle obligatoire pour toutes les bornes ?",
  "Elle est obligatoire au-delà de 3,7 kW. En dessous, elle n'est pas exigée, mais elle reste indispensable pour que vos clients accèdent aux aides publiques."),
]

# ---------------------------------------------------------------- ARTICLE 2
A2_BODY = """
<p class="lead">Entre les devis, les dossiers Enedis, la facturation, le SAV et la supervision des bornes posées, un installateur IRVE jongle avec plusieurs métiers. Le bon logiciel, ou la bonne combinaison, change tout. Voici comment s'y retrouver en 2026.</p>

<h2 id="besoin">De quel logiciel un installateur IRVE a-t-il vraiment besoin ?</h2>
<p>Il faut distinguer deux familles d'outils, souvent confondues : le <strong>logiciel de gestion d'entreprise</strong> (devis, chantiers, facturation, SAV) et le <strong>logiciel de supervision des bornes</strong> (pilotage à distance, refacturation de l'énergie). La plupart des installateurs ont besoin des deux, mais pour des raisons différentes.</p>
<p>Le premier fait tourner votre activité au quotidien. Le second est un service que vous vendez à vos clients après la pose, et une source de revenu récurrent.</p>

<h2 id="gestion">Logiciel de gestion : devis, chantiers et facturation</h2>
<p>C'est le socle : centraliser les devis, suivre les chantiers et éditer les factures conformes (mention IRVE, TVA à 5,5 % ou 20 %). Quelques solutions du marché orientées métier :</p>
<ul>
  <li><strong>Hélios</strong> : pensé pour l'IRVE, avec devis bornes pour particuliers et copropriétés, gestion des dossiers Enedis et facturation.</li>
  <li><strong>Technic-Soft (Service 9000)</strong> : GMAO et SAV pour installateurs et mainteneurs, suivi du parc, maintenance préventive et contrats avec garantie de rétablissement.</li>
  <li><strong>Logiciels de gestion généralistes</strong> (CRM ou ERP du bâtiment) : valables si votre activité IRVE reste une part d'une entreprise d'électricité plus large.</li>
</ul>
<p>Le bon réflexe : vérifier que l'outil gère la mention IRVE et le bon taux de TVA sur les documents, deux points de contrôle des dossiers d'aides.</p>

<div class="ctamid"><h3>Vous êtes installateur qualifié IRVE ?</h3><p>Recevez des demandes de particuliers et copropriétés qualifiées en amont.</p><a href="../partenaires.html">Rejoindre le réseau Les Éclairés</a></div>

<h2 id="supervision">Logiciel de supervision : piloter et refacturer les bornes</h2>
<p>La supervision est un logiciel qui dialogue avec les bornes installées (via le protocole OCPP) pour les piloter, mesurer la consommation au kWh et automatiser la refacturation. C'est ce qui permet à une copropriété ou une entreprise de répartir les coûts entre résidents, salariés ou centres de coûts.</p>
<ul>
  <li><strong>Refacturation automatique</strong> de l'énergie consommée, à l'usager ou au centre de coûts.</li>
  <li><strong>Gestion des droits d'accès</strong> (badges, utilisateurs autorisés).</li>
  <li><strong>Alertes de maintenance</strong> en cas de dysfonctionnement, utiles pour votre SAV.</li>
</ul>
<p>Des acteurs comme Chargekeeper ou Greenspot proposent des offres de supervision, y compris des licences pensées pour les installateurs qui veulent revendre le service. En copropriété, la supervision est souvent la contrepartie logique du <a href="financement-infrastructure-collective-copropriete-advenir-2026.html">financement de l'infrastructure collective</a>.</p>

<h2 id="prioriser">Gestion ou supervision : quelles fonctions prioriser ?</h2>
<p>Les deux familles ne répondent pas aux mêmes besoins. Ce tableau aide à ne pas payer pour des fonctions qui ne servent pas votre modèle.</p>
<table>
  <thead><tr><th>Besoin</th><th>Type d'outil</th></tr></thead>
  <tbody>
    <tr><td>Éditer devis et factures conformes IRVE</td><td>Gestion d'entreprise</td></tr>
    <tr><td>Suivre chantiers, planning et SAV</td><td>Gestion / GMAO</td></tr>
    <tr><td>Monter les dossiers Enedis et aides</td><td>Gestion métier IRVE</td></tr>
    <tr><td>Piloter les bornes à distance (OCPP)</td><td>Supervision</td></tr>
    <tr><td>Refacturer l'énergie en copro ou entreprise</td><td>Supervision</td></tr>
  </tbody>
</table>

<h2 id="choisir">Comment choisir la bonne solution en 2026 ?</h2>
<p>Réponse courte : partez de vos chantiers types, pas de la liste de fonctions. Quelques critères qui font vraiment la différence :</p>
<ul>
  <li><strong>Compatibilité OCPP</strong> pour la supervision, afin de ne pas être enfermé sur une seule marque de borne.</li>
  <li><strong>Gestion des dossiers ADVENIR et Enedis</strong> intégrée, pour gagner du temps sur l'administratif.</li>
  <li><strong>Refacturation</strong> fiable si vous visez la copropriété et l'entreprise.</li>
  <li><strong>Module SAV et maintenance</strong>, car un parc installé se pilote dans la durée.</li>
  <li><strong>Tarif et modèle</strong> (licence unique, abonnement, part revendable au client).</li>
</ul>
<p>Enfin, un outil ne remplace pas la qualification : c'est elle qui rend vos chantiers éligibles aux aides. Si le sujet vous concerne, voyez comment <a href="devenir-installateur-agree-advenir.html">devenir installateur agréé ADVENIR</a>.</p>

<h2 id="faq">Questions fréquentes</h2>
<h3>Un installateur IRVE a-t-il besoin d'un logiciel de supervision ?</h3>
<p>Pas pour poser une borne, mais c'est indispensable dès qu'il faut piloter et refacturer l'énergie, notamment en copropriété et en entreprise. C'est aussi un service récurrent à revendre.</p>
<h3>Qu'est-ce que le protocole OCPP ?</h3>
<p>C'est un standard ouvert de communication entre les bornes et les plateformes de supervision. Choisir une solution compatible OCPP évite d'être verrouillé sur une seule marque de matériel.</p>
<h3>Un logiciel gère-t-il les dossiers ADVENIR ?</h3>
<p>Certains logiciels métier IRVE intègrent le montage des dossiers d'aides et Enedis. Le dépôt ADVENIR reste toutefois fait par le bénéficiaire ou l'opérateur, avant les travaux.</p>
"""
A2_TOC = [("besoin","De quel logiciel un installateur IRVE a-t-il besoin ?"),
          ("gestion","Logiciel de gestion : devis, chantiers, facturation"),
          ("supervision","Logiciel de supervision : piloter et refacturer"),
          ("prioriser","Gestion ou supervision : quoi prioriser ?"),
          ("choisir","Comment choisir la bonne solution en 2026 ?"),
          ("faq","Questions fréquentes")]
A2_FAQ = [
 ("Un installateur IRVE a-t-il besoin d'un logiciel de supervision ?",
  "Pas pour poser une borne, mais c'est indispensable dès qu'il faut piloter et refacturer l'énergie, notamment en copropriété et en entreprise. C'est aussi un service récurrent à revendre."),
 ("Qu'est-ce que le protocole OCPP ?",
  "C'est un standard ouvert de communication entre les bornes et les plateformes de supervision. Choisir une solution compatible OCPP évite d'être verrouillé sur une seule marque de matériel."),
 ("Un logiciel gère-t-il les dossiers ADVENIR ?",
  "Certains logiciels métier IRVE intègrent le montage des dossiers d'aides et Enedis. Le dépôt ADVENIR reste toutefois fait par le bénéficiaire ou l'opérateur, avant les travaux."),
]

ARTICLES = [
 dict(slug="devenir-installateur-agree-advenir",
      seo_title="Installateur agréé ADVENIR : conditions et démarches",
      title="Devenir installateur agréé ADVENIR : conditions et démarches",
      meta="Installateur agréé ADVENIR : la qualification IRVE (Qualifelec ou AFNOR) rend vos chantiers éligibles à la prime. Conditions, démarches et barèmes 2026.",
      category="Espace pro", date="2026-09-14", date_fr="14 septembre 2026", read="7 min",
      excerpt="Installateur agréé ADVENIR : la qualification IRVE, les conditions, les démarches et les barèmes 2026 pour rendre vos chantiers éligibles.",
      thumb_svg='<svg viewBox="0 0 24 24" fill="none" stroke="#5ee0a6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 7l-9 9-5-5"/><path d="M3 12a9 9 0 1018 0 9 9 0 00-18 0z"/></svg>',
      body=A1_BODY, toc=A1_TOC, faq=A1_FAQ),
 dict(slug="logiciel-gestion-installateur-irve",
      seo_title="Quel logiciel de gestion pour installateur IRVE ?",
      title="Quel logiciel de gestion pour installateur IRVE ?",
      meta="Logiciel de gestion pour installateur IRVE : devis, dossiers Enedis, facturation et supervision des bornes. Comment choisir la bonne solution en 2026.",
      category="Espace pro", date="2026-09-14", date_fr="14 septembre 2026", read="6 min",
      excerpt="Logiciel de gestion pour installateur IRVE : gestion d'entreprise ou supervision des bornes, quelles fonctions prioriser et comment choisir en 2026.",
      thumb_svg='<svg viewBox="0 0 24 24" fill="none" stroke="#5ee0a6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 20h8"/><path d="M12 18v2"/><path d="M7 9l2 2-2 2"/><path d="M13 13h4"/></svg>',
      body=A2_BODY, toc=A2_TOC, faq=A2_FAQ),
]

def build_seo_block(a):
    url = f"{BASE}/blog/{a['slug']}.html"
    img = f"{BASE}/hero.jpg"
    bp = {"@context":"https://schema.org","@type":"BlogPosting","headline":a["seo_title"],
          "description":a["meta"],"image":img,"url":url,
          "mainEntityOfPage":{"@type":"WebPage","@id":url},
          "datePublished":a["date"],"dateModified":a["date"],
          "author":{"@type":"Organization","name":"Les Éclairés","url":f"{BASE}/"},
          "publisher":{"@type":"Organization","name":"Les Éclairés","logo":{"@type":"ImageObject","url":f"{BASE}/favicon.png"}}}
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Accueil","item":f"{BASE}/"},
          {"@type":"ListItem","position":2,"name":"Blog","item":f"{BASE}/blog/"},
          {"@type":"ListItem","position":3,"name":a["seo_title"],"item":url}]}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
          {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a["faq"]]}
    j = lambda d: json.dumps(d, ensure_ascii=False, separators=(",",":"))
    return (f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:title" content="{a["seo_title"]}">\n'
            f'<meta property="og:image" content="{img}">\n'
            f'<meta property="article:modified_time" content="{a["date"]}T00:00:00+01:00">\n'
            f'<script type="application/ld+json">{j(bp)}</script>\n'
            f'<script type="application/ld+json">{j(bc)}</script>\n'
            f'<script type="application/ld+json">{j(fq)}</script>\n')

def gen_article(a):
    html = TPL
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i,t in a["toc"])
    repl = {"%%SEO_TITLE%%":a["seo_title"],"%%META_DESC%%":a["meta"],"%%SLUG%%":a["slug"],
            "%%DATE_ISO%%":a["date"],"%%CATEGORY%%":a["category"],"%%TITRE%%":a["title"],
            "%%DATE_FR%%":a["date_fr"],"%%READ_TIME%%":a["read"],"%%TOC_ITEMS%%":toc,
            "%%ARTICLE_HTML%%":a["body"]}
    for k,v in repl.items():
        html = html.replace(k,v)
    assert "%%" not in html, "placeholder résiduel"
    html = html.replace("</head>", build_seo_block(a)+"</head>", 1)
    (BLOG / f"{a['slug']}.html").write_text(html, encoding="utf-8")
    print(f"  + article écrit : blog/{a['slug']}.html")

def register_sitemap():
    sm = (ROOT/"sitemap.xml").read_text(encoding="utf-8")
    add=""
    for a in ARTICLES:
        loc=f"{BASE}/blog/{a['slug']}.html"
        if loc in sm: continue
        add+=f"<url><loc>{loc}</loc><lastmod>{a['date']}</lastmod><priority>0.7</priority></url>\n"
    if add:
        sm = sm.replace("</urlset>", add+"</urlset>")
        (ROOT/"sitemap.xml").write_text(sm, encoding="utf-8")
        print("  + sitemap.xml mis à jour")

def register_listing():
    f = BLOG/"index.html"; t=f.read_text(encoding="utf-8")
    cards=""
    for a in reversed(ARTICLES):  # le plus récent en tête
        href=f"/blog/{a['slug']}.html"
        if href in t: continue
        cards+=(f'          <a class="blog-card" href="{href}">\n'
                f'          <span class="bc-tag">{a["category"]}</span>\n'
                f'          <span class="bc-date">{a["date_fr"].split(" ",1)[1].capitalize()}</span>\n'
                f'          <h2>{a["title"]}</h2>\n'
                f'          <p>{a["excerpt"]}</p>\n'
                f'          <span class="bc-more">Lire l\'article →</span>\n'
                f'        </a>\n')
    if cards:
        t=t.replace('<div class="blog-grid">', '<div class="blog-grid">\n'+cards, 1)
        f.write_text(t, encoding="utf-8"); print("  + blog/index.html (listing) mis à jour")

def register_home():
    f = ROOT/"index.html"; t=f.read_text(encoding="utf-8")
    if f"blog/{ARTICLES[0]['slug']}.html" in t:
        print("  = accueil déjà à jour"); return
    cards=[]
    rd=["rd1","rd2","rd3"]
    picks = ARTICLES + [dict(slug="borne-recharge-chambery-installateur-aides-2026",
                             category="Installation & Bornes", date_fr="14 septembre 2026",
                             title="Borne de recharge à Chambéry : installateur et aides 2026",
                             excerpt="Borne de recharge Chambéry : trouvez un installateur certifié et toutes les aides disponibles en 2026. Guide gratuit et indépendant.",
                             thumb_svg='<svg viewBox="0 0 24 24" fill="none" stroke="#5ee0a6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2v6"/><path d="M15 2v6"/><path d="M6 8h12v3a6 6 0 01-12 0V8z"/><path d="M12 17v5"/></svg>')]
    for i,a in enumerate(picks[:3]):
        mois=a["date_fr"].split(" ",1)[1].capitalize()
        cards.append(
          f'      <a href="blog/{a["slug"]}.html" class="blog-card reveal {rd[i]}">\n'
          f'        <div class="blog-thumb">\n          {a["thumb_svg"]}\n'
          f'          <span class="blog-tag">{a["category"]}</span>\n        </div>\n'
          f'        <div class="blog-body">\n          <div class="blog-date">{mois}</div>\n'
          f'          <div class="blog-title">{a["title"]}</div>\n'
          f'          <div class="blog-excerpt">{a["excerpt"]}</div>\n'
          f'          <span class="blog-cta">Lire l\'article →</span>\n        </div>\n      </a>')
    new_grid = '<div class="blog-grid">\n'+"\n".join(cards)+"\n    </div>"
    # remplace le bloc blog-grid de la section blog (celui qui contient les cartes blog-card reveal)
    m = re.search(r'<div class="blog-grid">\s*\n\s*<a href="blog/.*?</a>\s*\n\s*</div>', t, re.S)
    assert m, "bloc carrousel accueil introuvable"
    t = t[:m.start()] + new_grid + t[m.end():]
    f.write_text(t, encoding="utf-8"); print("  + index.html (carrousel accueil) mis à jour")

def add_inbound_link():
    # lien entrant vers l'article 1 depuis choisir-installateur (évite un orphelin)
    f = BLOG/"choisir-installateur-irve-certifie.html"; t=f.read_text(encoding="utf-8")
    if "devenir-installateur-agree-advenir.html" in t:
        print("  = lien entrant déjà présent"); return
    anchor = "</main>"
    note = ('<p><em>Vous êtes vous-même installateur ? Voyez comment '
            '<a href="devenir-installateur-agree-advenir.html">devenir installateur agréé ADVENIR</a> '
            'et quel <a href="logiciel-gestion-installateur-irve.html">logiciel de gestion IRVE</a> choisir.</em></p>\n')
    if anchor in t:
        t = t.replace(anchor, note+anchor, 1)
        f.write_text(t, encoding="utf-8"); print("  + lien entrant ajouté depuis choisir-installateur")
    else:
        print("  ! ancre </main> introuvable dans choisir-installateur")

print("=== GÉNÉRATION ARTICLES B2B ===")
for a in ARTICLES: gen_article(a)
register_sitemap()
register_listing()
register_home()
add_inbound_link()
print("Terminé.")
