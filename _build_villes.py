#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les pages villes (full SEO) + la page /copropriete, en réutilisant
la D.A. (CSS + assets) de la page Lyon existante."""
import re, json

REF = open('villes/borne-recharge-lyon.html', encoding='utf-8').read()
def _between(a, b, s=REF):
    i = s.index(a); j = s.index(b, i + len(a)); return s[i:j + len(b)]

CSS     = _between('<style>', '</style>')
FAVICON = _between('<link rel="icon"', '>')
FONTS   = _between('<link href="https://fonts.googleapis.com', '>')
NAVLOGO = re.search(r'nav-logo[^>]*><img src="(data:[^"]+)"', REF).group(1)
FOOTLOGO = re.search(r'footer-bottom-logo" src="(data:[^"]+)"', REF).group(1)

GA = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZXGFCVHHDM"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-ZXGFCVHHDM');
</script>'''

PRELOADER = '<div id="preloader" role="status" aria-label="Chargement"><div class="pl-logo"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13 2L4 13.5h6.2L9 22l9-12.5h-6.2L13 2z"/></svg></div><span class="pl-name">Les Éclairés</span><div class="pl-bar"><i></i></div></div>'

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'

EXTRA_CSS = '''<style>
.breadcrumb{font-size:13px;color:var(--c-muted);margin-bottom:18px}
.breadcrumb a{color:var(--c-muted);text-decoration:none}.breadcrumb a:hover{color:var(--c-vert)}
.breadcrumb span{color:var(--c-text)}
.copro-box{background:var(--c-vert-bg);border:1px solid var(--c-vert-br);border-radius:var(--r-xl);padding:32px;margin:8px 0 48px}
.copro-box h3{font-family:var(--ff-h);font-size:21px;font-weight:800;letter-spacing:-.03em;color:var(--c-ink);margin:0 0 10px}
.copro-box p{font-size:15px;line-height:1.65;color:var(--c-text);margin:0 0 18px}
.faq-city{margin-bottom:48px}
.faq-city details{border:1px solid var(--c-border);border-radius:var(--r-lg);margin-bottom:12px;background:var(--c-bg2);overflow:hidden}
.faq-city summary{cursor:pointer;list-style:none;padding:20px 24px;font-family:var(--ff-h);font-weight:700;font-size:16px;color:var(--c-ink);display:flex;justify-content:space-between;align-items:center;gap:16px}
.faq-city summary::-webkit-details-marker{display:none}
.faq-city summary::after{content:'+';font-size:24px;color:var(--c-vert);font-weight:400;flex-shrink:0;line-height:1}
.faq-city details[open] summary::after{content:'\\2212'}
.faq-city details>div{padding:0 24px 20px;font-size:15px;line-height:1.7;color:var(--c-mid)}
.faq-city details>div a{color:var(--c-vert);font-weight:600;text-decoration:none}
.related{margin:0 0 48px;font-size:15px;color:var(--c-mid);line-height:1.8}
.related a{color:var(--c-vert);text-decoration:none;font-weight:600}
.footer-cities{margin-top:40px;padding-top:32px;border-top:1px solid var(--c-border)}
.footer-cities h4{font-family:var(--ff-h);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-muted);margin-bottom:16px}
.footer-cities-list{list-style:none;margin:0;padding:0;column-count:4;column-gap:32px}
.footer-cities-list li{margin-bottom:9px;break-inside:avoid}
.footer-cities-list a{color:var(--c-mid);text-decoration:none;font-size:14px}.footer-cities-list a:hover{color:var(--c-vert)}
@media(max-width:860px){.footer-cities-list{column-count:2}}
@media(max-width:520px){.footer-cities-list{column-count:1}}
</style>'''

# ---- Liste complète des villes (maillage + footer) ----
ALL_CITIES = [
 ('aix-en-provence','Aix-en-Provence'),('annecy','Annecy'),('lyon','Lyon'),
 ('nantes','Nantes'),('bordeaux','Bordeaux'),('montpellier','Montpellier'),
 ('toulouse','Toulouse'),('rennes','Rennes'),('la-rochelle','La Rochelle'),
 ('chambery','Chambéry'),('valence','Valence'),('grenoble','Grenoble'),
 ('angers','Angers'),('poitiers','Poitiers'),('vannes','Vannes'),('pau','Pau'),
 ('niort','Niort'),('clermont-ferrand','Clermont-Ferrand'),('tours','Tours'),
 ('metz','Metz'),('paris','Paris'),('marseille','Marseille'),
 ('strasbourg','Strasbourg'),('saint-etienne','Saint-Étienne'),('corse','Corse'),
]
REGION = {
 'aix-en-provence':"Provence-Alpes-Côte d'Azur",'marseille':"Provence-Alpes-Côte d'Azur",
 'annecy':'Auvergne-Rhône-Alpes','lyon':'Auvergne-Rhône-Alpes','chambery':'Auvergne-Rhône-Alpes',
 'valence':'Auvergne-Rhône-Alpes','grenoble':'Auvergne-Rhône-Alpes','clermont-ferrand':'Auvergne-Rhône-Alpes',
 'saint-etienne':'Auvergne-Rhône-Alpes','nantes':'Pays de la Loire','angers':'Pays de la Loire',
 'bordeaux':'Nouvelle-Aquitaine','la-rochelle':'Nouvelle-Aquitaine','poitiers':'Nouvelle-Aquitaine',
 'pau':'Nouvelle-Aquitaine','niort':'Nouvelle-Aquitaine','toulouse':'Occitanie','montpellier':'Occitanie',
 'rennes':'Bretagne','vannes':'Bretagne','tours':'Centre-Val de Loire','metz':'Grand Est',
 'strasbourg':'Grand Est','paris':'Île-de-France','corse':'Corse',
}
LABEL = dict(ALL_CITIES)
CODE = {
 'aix-en-provence':'13','annecy':'74','lyon':'69','nantes':'44','bordeaux':'33',
 'montpellier':'34','toulouse':'31','rennes':'35','la-rochelle':'17','chambery':'73',
 'valence':'26','grenoble':'38','angers':'49','poitiers':'86','vannes':'56','pau':'64',
 'niort':'79','clermont-ferrand':'63','tours':'37','metz':'57','paris':'75',
 'marseille':'13','strasbourg':'67','saint-etienne':'42','corse':'2A/2B',
}
# Villes phares affichées dans le footer (le reste via la page hub /villes)
FLAGSHIP = ['aix-en-provence','annecy','lyon','nantes','bordeaux','montpellier','toulouse','rennes']
REGION_ORDER = ["Auvergne-Rhône-Alpes","Nouvelle-Aquitaine","Occitanie",
  "Provence-Alpes-Côte d'Azur","Pays de la Loire","Bretagne","Grand Est",
  "Centre-Val de Loire","Île-de-France","Corse"]

def footer_cities():
    lis = '\n'.join(
      f'          <li><a href="/villes/borne-recharge-{sl}.html">Borne de recharge {LABEL[sl]}</a></li>'
      for sl in FLAGSHIP)
    return f'''    <div class="footer-cities">
      <h4>Guides par ville</h4>
      <ul class="footer-cities-list">
{lis}
          <li><a href="/villes"><strong>Toutes les villes →</strong></a></li>
      </ul>
    </div>'''

def footer(rel_root='/'):
    return f'''<footer>
  <div class="footer-top">
    <div class="footer-cols">
      <div class="footer-col">
        <h4>Le service</h4>
        <ul>
          <li><a href="/simulateur">Simulateur IRVE</a></li>
          <li><a href="/copropriete">Bornes en copropriété</a></li>
          <li><a href="/partenaires.html">Devenir partenaire</a></li>
          <li><a href="/#histoire">Notre histoire</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Ressources</h4>
        <ul>
          <li><a href="/blog/">Blog IRVE</a></li>
          <li><a href="https://www.ecologie.gouv.fr/sites/default/files/documents/Convention%20Advenir%20sign%C3%A9e.pdf" target="_blank" rel="noopener">Prime ADVENIR ↗</a></li>
          <li><a href="https://www.avere-france.org/" target="_blank" rel="noopener">AVERE-France ↗</a></li>
          <li><a href="https://www.irve.gouv.fr/" target="_blank" rel="noopener">IRVE.gouv.fr ↗</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations</h4>
        <ul>
          <li><a href="/mentions-legales.html">Mentions légales</a></li>
          <li><a href="/confidentialite.html">Confidentialité</a></li>
          <li><a href="mailto:contact@leseclaires.fr">Nous écrire</a></li>
        </ul>
      </div>
    </div>
{footer_cities()}
  </div>
  <div class="footer-bottom">
    <span class="footer-brand-group" style="display:inline-flex;align-items:center;gap:10px"><img class="footer-bottom-logo" src="{FOOTLOGO}" alt="Les Éclairés" style="height:24px;width:auto;border-radius:6px;display:block;flex-shrink:0"><span class="f-brand-name">Les Éclairés</span></span>
    <span class="footer-legal">© 2026 Les Éclairés · Comprendre, choisir, installer.</span>
  </div>
</footer>'''

AIDE_CARDS = '''  <div class="info-grid">
    <div class="info-card">
      <h4>Crédit d'impôt à domicile</h4>
      <span class="amount">75 %</span>
      <p>Pour les maisons individuelles. Jusqu'à 500 € remboursés sur votre installation. Valable pour les propriétaires et les locataires.</p>
    </div>
    <div class="info-card">
      <h4>Prime ADVENIR (copropriété)</h4>
      <span class="amount">960 €</span>
      <p>Par point de charge en copropriété. Cette aide peut couvrir une grande partie du coût. La demande se fait avant les travaux.</p>
    </div>
    <div class="info-card">
      <h4>Budget moyen constaté</h4>
      <span class="amount">600 à 1 400 €</span>
      <p>Pour une maison individuelle, tout compris. Après aides, votre reste à charge est souvent inférieur à 500 €.</p>
    </div>
    <div class="info-card">
      <h4>Délai d'installation</h4>
      <span class="amount">2 à 4 semaines</span>
      <p>Pour une maison avec tableau électrique récent. En copropriété, les démarches peuvent prendre un peu plus de temps.</p>
    </div>
  </div>'''

STEPS = '''  <div class="info-grid">
    <div class="info-card"><h4>1. Simulateur gratuit</h4><p>Répondez à quelques questions simples sur votre logement et votre véhicule. Vous recevez immédiatement une recommandation personnalisée.</p></div>
    <div class="info-card"><h4>2. Mise en relation</h4><p>On vous met en contact avec un électricien certifié IRVE dans votre secteur. Un seul contact, pas une liste à éplucher.</p></div>
    <div class="info-card"><h4>3. Installation</h4><p>Vous savez exactement ce que vous allez payer et les aides que vous allez toucher avant que les travaux commencent.</p></div>
    <div class="info-card"><h4>100 % gratuit pour vous</h4><p>Le simulateur et les conseils sont entièrement gratuits. On est rémunérés par l'installateur, pas par vous.</p></div>
  </div>'''

def faq_block(name, dept):
    qa = [
     (f"Combien coûte l'installation d'une borne de recharge à {name} ?",
      f"Pour une maison individuelle à {name}, comptez en général entre 600 et 1&nbsp;400&nbsp;€ tout compris (matériel et pose). Après le crédit d'impôt (jusqu'à 500&nbsp;€), votre reste à charge descend souvent sous les 500&nbsp;€. En copropriété, le budget dépend du nombre de points de charge installés."),
     (f"Quelles aides puis-je obtenir à {name} ?",
      f"À {name}, vous pouvez selon votre situation cumuler le crédit d'impôt de 75&nbsp;% (maison individuelle), la prime ADVENIR (copropriété et entreprise), une TVA réduite et d'éventuelles aides locales. Le simulateur vous indique en quelques clics celles auxquelles vous êtes éligible."),
     (f"Puis-je installer une borne en copropriété à {name} ?",
      f"Oui. Que vous soyez propriétaire ou locataire à {name}, le «&nbsp;droit à la prise&nbsp;» vous permet d'installer une borne sur votre place de parking. La prime ADVENIR peut financer une grande partie d'un projet collectif. <a href=\"/copropriete\">En savoir plus sur les bornes en copropriété</a>."),
     (f"Combien de temps prend l'installation à {name} ?",
      f"Pour une maison avec un tableau électrique récent à {name}, comptez 2 à 4 semaines entre la prise de contact et l'installation. En copropriété, les démarches administratives rallongent un peu le délai."),
     ("Quelle puissance de borne choisir ?",
      "Une borne de 7,4&nbsp;kW suffit dans la grande majorité des cas : elle recharge votre véhicule en une nuit. Une puissance supérieure (11 ou 22&nbsp;kW) se justifie pour plusieurs véhicules ou un usage professionnel. Le simulateur vous recommande la puissance adaptée."),
     ("Le service Les Éclairés est-il gratuit ?",
      f"Oui, à {name} comme partout en France, le simulateur et nos conseils sont 100&nbsp;% gratuits et sans engagement. Nous sommes rémunérés par l'installateur partenaire, jamais par vous."),
    ]
    html = '\n'.join(
      f'    <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in qa)
    ld = [{"@type":"Question","name":q,
           "acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a).replace('\xa0',' ')}}
          for q, a in qa]
    return html, ld

def related(slug):
    reg = REGION[slug]
    sibs = [(sl,lb) for sl,lb in ALL_CITIES if sl!=slug and REGION.get(sl)==reg][:4]
    if not sibs: return ''
    links = ', '.join(f'<a href="/villes/borne-recharge-{sl}.html">{lb}</a>' for sl,lb in sibs)
    return f'  <p class="related">Autres villes en {reg} : {links}.</p>\n'

# ---------------- Données des 17 villes ----------------
CITIES = [
 dict(slug='aix-en-provence', name='Aix-en-Provence', dept='Bouches-du-Rhône', code='13',
   in_dept='dans les Bouches-du-Rhône',
   sub="Vous habitez Aix-en-Provence et vous souhaitez installer une borne de recharge chez vous ? On vous accompagne pas à pas, gratuitement. Maison à Puyricard, appartement en centre-ville ou résidence au Tholonet : on trouve la solution adaptée à votre véhicule.",
   local="Aix-en-Provence est l'une des villes françaises où l'adoption du véhicule électrique progresse le plus vite, portée par un fort taux de propriétaires de maisons individuelles et une réelle sensibilité environnementale. Le réseau d'installateurs certifiés IRVE dans les Bouches-du-Rhône est dense, ce qui garantit des délais courts, y compris dans les communes périphériques.",
   zones="Aix centre, Puyricard, Luynes, Les Milles, Le Tholonet, Venelles, Éguilles, Bouc-Bel-Air, Meyreuil"),
 dict(slug='nantes', name='Nantes', dept='Loire-Atlantique', code='44', in_dept='en Loire-Atlantique',
   sub="Vous vivez à Nantes ou dans son agglomération et vous voulez recharger votre voiture électrique à domicile ? On vous guide gratuitement. Maison avec jardin à Orvault, appartement sur l'Île de Nantes ou pavillon à Vertou : on adapte la recommandation à votre situation.",
   local="Nantes fait partie des métropoles les plus engagées dans la transition énergétique, avec un habitat pavillonnaire très répandu, idéal pour l'installation d'une borne à domicile. Nantes Métropole encourage la mobilité électrique, et les installateurs certifiés IRVE de Loire-Atlantique couvrent toute l'agglomération.",
   zones="Nantes, Rezé, Saint-Herblain, Orvault, Vertou, Carquefou, Bouguenais, Saint-Sébastien-sur-Loire, La Chapelle-sur-Erdre"),
 dict(slug='bordeaux', name='Bordeaux', dept='Gironde', code='33', in_dept='en Gironde',
   sub="Vous habitez Bordeaux ou sa métropole et vous envisagez d'installer une borne de recharge ? On vous accompagne gratuitement. Échoppe bordelaise, maison à Mérignac ou appartement à Talence : on trouve la borne qui correspond à votre logement et à votre véhicule.",
   local="Bordeaux connaît une forte croissance démographique et un afflux de nouveaux propriétaires, souvent dans des logements récents bien adaptés à la recharge électrique. La métropole soutient activement la mobilité propre, et les installateurs certifiés IRVE de Gironde assurent des délais d'intervention rapides.",
   zones="Bordeaux, Mérignac, Pessac, Talence, Bègles, Le Bouscat, Gradignan, Villenave-d'Ornon, Bruges"),
 dict(slug='toulouse', name='Toulouse', dept='Haute-Garonne', code='31', in_dept='en Haute-Garonne',
   sub="Vous résidez à Toulouse ou dans son agglomération et vous souhaitez une borne de recharge à domicile ? On vous guide gratuitement. Maison à Tournefeuille, appartement aux Carmes ou local d'entreprise à Blagnac : on trouve la solution adaptée.",
   local="La métropole toulousaine, en pleine expansion, compte de nombreux quartiers pavillonnaires propices à l'installation d'une borne individuelle. Le réseau d'installateurs certifiés IRVE de Haute-Garonne est étoffé et permet des interventions rapides sur toute l'agglomération.",
   zones="Toulouse, Blagnac, Colomiers, Tournefeuille, Balma, Ramonville-Saint-Agne, L'Union, Cugnaux, Saint-Orens-de-Gameville"),
 dict(slug='rennes', name='Rennes', dept='Ille-et-Vilaine', code='35', in_dept='en Ille-et-Vilaine',
   sub="Vous habitez Rennes ou sa métropole et vous voulez installer une borne de recharge chez vous ? On vous accompagne gratuitement, pas à pas. Maison à Cesson-Sévigné, appartement au centre ou pavillon à Bruz : on adapte la recommandation à votre projet.",
   local="Rennes est une métropole dynamique où la mobilité électrique se développe rapidement, soutenue par un habitat individuel important en périphérie. Les installateurs certifiés IRVE d'Ille-et-Vilaine couvrent l'ensemble du bassin rennais avec des délais maîtrisés.",
   zones="Rennes, Cesson-Sévigné, Bruz, Saint-Grégoire, Pacé, Chantepie, Saint-Jacques-de-la-Lande, Betton"),
 dict(slug='la-rochelle', name='La Rochelle', dept='Charente-Maritime', code='17', in_dept='en Charente-Maritime',
   sub="Vous vivez à La Rochelle ou ses environs et vous souhaitez recharger votre voiture électrique à domicile ? On vous guide gratuitement. Maison à Lagord, appartement près du Vieux-Port ou résidence à Aytré : on trouve la borne adaptée.",
   local="La Rochelle est une ville pionnière de la mobilité durable, avec une population sensible aux enjeux écologiques et un habitat individuel répandu. Les installateurs certifiés IRVE de Charente-Maritime interviennent rapidement sur toute l'agglomération rochelaise.",
   zones="La Rochelle, Aytré, Lagord, Périgny, Châtelaillon-Plage, Angoulins, Puilboreau, Nieul-sur-Mer"),
 dict(slug='chambery', name='Chambéry', dept='Savoie', code='73', in_dept='en Savoie',
   sub="Vous habitez Chambéry ou son agglomération et vous voulez installer une borne de recharge ? On vous accompagne gratuitement. Maison à Barberaz, appartement en centre-ville ou résidence à La Ravoire : on adapte la solution à votre logement.",
   local="Aux portes des Alpes, Chambéry bénéficie d'un fort taux d'équipement en véhicules électriques et d'un habitat individuel important. Les installateurs certifiés IRVE de Savoie connaissent bien les contraintes locales et interviennent rapidement.",
   zones="Chambéry, La Ravoire, Cognin, Barberaz, Jacob-Bellecombette, La Motte-Servolex, Bassens, Saint-Alban-Leysse"),
 dict(slug='valence', name='Valence', dept='Drôme', code='26', in_dept='dans la Drôme',
   sub="Vous résidez à Valence ou dans son agglomération et vous envisagez une borne de recharge à domicile ? On vous guide gratuitement. Maison à Bourg-lès-Valence, appartement au centre ou pavillon à Portes-lès-Valence : on trouve la bonne solution.",
   local="Idéalement située sur l'axe rhodanien, Valence voit la mobilité électrique se développer rapidement. L'habitat pavillonnaire y est très présent, ce qui facilite l'installation de bornes individuelles. Les installateurs certifiés IRVE de la Drôme assurent des délais courts.",
   zones="Valence, Bourg-lès-Valence, Portes-lès-Valence, Guilherand-Granges, Saint-Péray, Chabeuil, Beaumont-lès-Valence"),
 dict(slug='grenoble', name='Grenoble', dept='Isère', code='38', in_dept='en Isère',
   sub="Vous habitez Grenoble ou sa métropole et vous souhaitez installer une borne de recharge chez vous ? On vous accompagne gratuitement. Maison à Meylan, appartement en ville ou résidence à Échirolles : on adapte la recommandation à votre véhicule.",
   local="Grenoble, capitale alpine très engagée dans la transition écologique, affiche une adoption élevée du véhicule électrique. Les installateurs certifiés IRVE de l'Isère couvrent l'ensemble de la métropole et maîtrisent les spécificités locales.",
   zones="Grenoble, Saint-Martin-d'Hères, Échirolles, Meylan, Seyssinet-Pariset, Fontaine, Saint-Égrève, Eybens"),
 dict(slug='angers', name='Angers', dept='Maine-et-Loire', code='49', in_dept='en Maine-et-Loire',
   sub="Vous vivez à Angers ou dans son agglomération et vous voulez recharger votre voiture électrique à domicile ? On vous guide gratuitement. Maison à Avrillé, appartement au centre ou pavillon aux Ponts-de-Cé : on trouve la solution adaptée.",
   local="Régulièrement citée parmi les villes où il fait bon vivre, Angers conjugue habitat pavillonnaire et fort engagement environnemental. Les installateurs certifiés IRVE de Maine-et-Loire interviennent rapidement sur toute l'agglomération angevine.",
   zones="Angers, Avrillé, Trélazé, Les Ponts-de-Cé, Beaucouzé, Saint-Barthélemy-d'Anjou, Bouchemaine"),
 dict(slug='poitiers', name='Poitiers', dept='Vienne', code='86', in_dept='dans la Vienne',
   sub="Vous habitez Poitiers ou ses environs et vous envisagez une borne de recharge à domicile ? On vous accompagne gratuitement. Maison à Buxerolles, appartement en centre-ville ou pavillon à Saint-Benoît : on adapte la solution à votre projet.",
   local="Poitiers, ville résidentielle et étudiante, présente un habitat individuel répandu favorable à la recharge à domicile. Les installateurs certifiés IRVE de la Vienne couvrent l'agglomération avec des délais maîtrisés.",
   zones="Poitiers, Buxerolles, Saint-Benoît, Migné-Auxances, Chasseneuil-du-Poitou, Biard, Vouneuil-sous-Biard"),
 dict(slug='vannes', name='Vannes', dept='Morbihan', code='56', in_dept='dans le Morbihan',
   sub="Vous résidez à Vannes ou dans le golfe du Morbihan et vous souhaitez installer une borne de recharge ? On vous guide gratuitement. Maison à Arradon, appartement au centre ou résidence à Séné : on trouve la borne adaptée.",
   local="Sur les rives du golfe du Morbihan, Vannes attire de nombreux propriétaires de maisons individuelles, souvent récentes, avec une forte sensibilité environnementale. Les installateurs certifiés IRVE du Morbihan assurent des interventions rapides autour du golfe.",
   zones="Vannes, Séné, Arradon, Saint-Avé, Theix-Noyalo, Ploeren, Le Bono, Sarzeau"),
 dict(slug='pau', name='Pau', dept='Pyrénées-Atlantiques', code='64', in_dept='dans les Pyrénées-Atlantiques',
   sub="Vous habitez Pau ou son agglomération et vous voulez recharger votre voiture électrique à domicile ? On vous accompagne gratuitement. Maison à Jurançon, appartement au centre ou pavillon à Lons : on adapte la recommandation à votre logement.",
   local="Au pied des Pyrénées, Pau conjugue habitat individuel important et qualité de vie reconnue. La mobilité électrique s'y développe, et les installateurs certifiés IRVE des Pyrénées-Atlantiques couvrent l'ensemble de l'agglomération paloise.",
   zones="Pau, Lons, Billère, Lescar, Bizanos, Jurançon, Gan, Idron"),
 dict(slug='niort', name='Niort', dept='Deux-Sèvres', code='79', in_dept='dans les Deux-Sèvres',
   sub="Vous vivez à Niort ou dans ses environs et vous envisagez une borne de recharge à domicile ? On vous guide gratuitement. Maison à Chauray, appartement au centre ou pavillon à Aiffres : on trouve la solution adaptée.",
   local="Niort, important pôle économique du Centre-Ouest, présente un habitat pavillonnaire répandu et un fort taux de propriétaires. Les installateurs certifiés IRVE des Deux-Sèvres interviennent rapidement sur l'agglomération niortaise.",
   zones="Niort, Chauray, Bessines, Aiffres, Échiré, Saint-Liguaire, Magné, Coulon"),
 dict(slug='clermont-ferrand', name='Clermont-Ferrand', dept='Puy-de-Dôme', code='63', in_dept='dans le Puy-de-Dôme',
   sub="Vous habitez Clermont-Ferrand ou sa métropole et vous souhaitez installer une borne de recharge ? On vous accompagne gratuitement. Maison à Chamalières, appartement en ville ou pavillon à Cournon : on adapte la solution à votre véhicule.",
   local="Au cœur de l'Auvergne, Clermont-Ferrand voit la mobilité électrique progresser, portée par un habitat individuel important en périphérie. Les installateurs certifiés IRVE du Puy-de-Dôme couvrent l'ensemble de la métropole clermontoise.",
   zones="Clermont-Ferrand, Aubière, Beaumont, Chamalières, Cournon-d'Auvergne, Riom, Royat, Gerzat"),
 dict(slug='tours', name='Tours', dept='Indre-et-Loire', code='37', in_dept='en Indre-et-Loire',
   sub="Vous résidez à Tours ou dans son agglomération et vous voulez recharger votre voiture électrique à domicile ? On vous guide gratuitement. Maison à Saint-Cyr-sur-Loire, appartement au centre ou pavillon à Joué-lès-Tours : on trouve la borne adaptée.",
   local="Au cœur du Val de Loire, Tours bénéficie d'un habitat pavillonnaire étendu et d'une bonne dynamique de la mobilité électrique. Les installateurs certifiés IRVE d'Indre-et-Loire assurent des délais d'intervention courts sur l'agglomération tourangelle.",
   zones="Tours, Joué-lès-Tours, Saint-Cyr-sur-Loire, Saint-Avertin, La Riche, Chambray-lès-Tours, Saint-Pierre-des-Corps, Fondettes"),
 dict(slug='metz', name='Metz', dept='Moselle', code='57', in_dept='en Moselle',
   sub="Vous habitez Metz ou son agglomération et vous envisagez une borne de recharge à domicile ? On vous accompagne gratuitement. Maison à Montigny-lès-Metz, appartement au centre ou pavillon à Marly : on adapte la recommandation à votre projet.",
   local="Metz, ville-jardin du Grand Est, conjugue habitat individuel important et engagement croissant dans la mobilité propre. Les installateurs certifiés IRVE de Moselle couvrent l'ensemble de l'agglomération messine avec des délais maîtrisés.",
   zones="Metz, Montigny-lès-Metz, Woippy, Marly, Le Ban-Saint-Martin, Longeville-lès-Metz, Saint-Julien-lès-Metz, Ars-sur-Moselle"),
]

def build_city(c):
    name, slug, dept, code = c['name'], c['slug'], c['dept'], c['code']
    region = REGION[slug]
    url = f"https://leseclaires.fr/villes/borne-recharge-{slug}.html"
    desc = f"Installer une borne de recharge électrique à {name} ({code}) : aides ADVENIR, prix, crédit d'impôt et installateurs certifiés IRVE {c['in_dept']}. Simulateur gratuit."
    faq_html, faq_ld = faq_block(name, dept)
    graph = {
      "@context":"https://schema.org",
      "@graph":[
        {"@type":"Service","name":f"Installation borne de recharge {name}","description":desc,
         "provider":{"@type":"Organization","name":"Les Éclairés","url":"https://leseclaires.fr"},
         "areaServed":{"@type":"City","name":name,
           "containedInPlace":{"@type":"AdministrativeArea","name":region}},
         "url":url},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Accueil","item":"https://leseclaires.fr/"},
          {"@type":"ListItem","position":2,"name":"Bornes par ville","item":"https://leseclaires.fr/villes"},
          {"@type":"ListItem","position":3,"name":name,"item":url}]},
        {"@type":"FAQPage","mainEntity":faq_ld},
      ]}
    jsonld = '<script type="application/ld+json">\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n</script>'
    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Borne de recharge à {name} ({code}) : aides, prix &amp; simulateur | Les Éclairés</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="borne de recharge {name}, installation borne {name}, IRVE {name}, prime ADVENIR {dept}, wallbox {name}, simulateur borne {name}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Borne de recharge à {name} | Les Éclairés">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://leseclaires.fr/nous-les-eclaires.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Borne de recharge à {name} | Les Éclairés">
<meta name="twitter:description" content="{desc}">
{FAVICON}
{FONTS}
{jsonld}
{CSS}
{EXTRA_CSS}
<noscript><style>#preloader{{display:none!important}}</style></noscript>
</head>
<body>
{PRELOADER}
<nav>
  <a class="nav-logo" href="../index.html"><img src="{NAVLOGO}" alt="Les Éclairés"><span>Les Éclairés</span></a>
  <a class="btn-nav" href="/simulateur">Simuler mon projet</a>
</nav>

<div class="hero-city">
  <div class="breadcrumb"><a href="/">Accueil</a> › <a href="/villes">Bornes par ville</a> › <span>{name}</span></div>
  <div class="city-badge"><span class="badge-dot"></span>Guide gratuit · {dept} ({code})</div>
  <h1 class="city-h1">Installer une borne de recharge<br><span style="white-space:nowrap">à {name}</span></h1>
  <p class="city-sub">{c['sub']}</p>
  <a href="/simulateur" class="btn-primary">Démarrer le simulateur gratuit {ARROW}</a>
</div>

<div class="city-body">

  <span class="section-tag">Ce qu'il faut savoir</span>
  <h2 class="section-h2">Les aides disponibles à {name}</h2>
  <p class="section-lead">Plusieurs aides peuvent financer une grande partie de votre installation. Voici les principales.</p>
{AIDE_CARDS}

  <span class="section-tag">Spécificités locales</span>
  <h2 class="section-h2">L'installation de bornes à {name}</h2>
  <p class="section-lead">{c['local']}</p>

  <div class="areas-section">
    <h4>Zones couvertes</h4>
    <p>{c['zones']}</p>
  </div>

  <div class="copro-box">
    <h3>Vous êtes en copropriété ou syndic à {name} ?</h3>
    <p>Équiper une copropriété, c'est souvent plusieurs dizaines de bornes à installer. On accompagne les conseils syndicaux et les syndics de A à Z : droit à la prise, prime ADVENIR collective, infrastructure évolutive.</p>
    <a href="/copropriete" class="btn-vert">Bornes en copropriété {ARROW}</a>
  </div>

  <span class="section-tag">Comment ça marche</span>
  <h2 class="section-h2">Trois étapes pour installer votre borne</h2>
{STEPS}

  <span class="section-tag">Questions fréquentes</span>
  <h2 class="section-h2">Borne de recharge à {name} : vos questions</h2>
  <div class="faq-city">
{faq_html}
  </div>

{related(slug)}
  <div class="cta-box">
    <h3>Prêt à installer votre borne à {name} ?</h3>
    <p>Répondez à quelques questions simples et recevez votre recommandation personnalisée. Gratuit, immédiat, sans engagement.</p>
    <a href="/simulateur" class="btn-vert">Démarrer le simulateur {ARROW}</a>
  </div>

</div>

{footer()}
  <script src="/cursor.js" defer></script>
</body>
</html>
'''
    open(f'villes/borne-recharge-{slug}.html','w',encoding='utf-8').write(html)
    return len(html)

def copro_box(name):
    return f'''  <div class="copro-box">
    <h3>Vous êtes en copropriété ou syndic à {name} ?</h3>
    <p>Équiper une copropriété, c'est souvent plusieurs dizaines de bornes à installer. On accompagne les conseils syndicaux et les syndics de A à Z : droit à la prise, prime ADVENIR collective, infrastructure évolutive.</p>
    <a href="/copropriete" class="btn-vert">Bornes en copropriété {ARROW}</a>
  </div>

'''

HUB_CSS = '''<style>
.villes-region{margin-bottom:44px}
.villes-region h2{font-size:clamp(20px,2.6vw,28px);font-weight:800;letter-spacing:-.03em;margin:0 0 18px;color:var(--c-ink)}
.villes-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.villes-grid a{display:block;background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-lg);padding:16px 18px;text-decoration:none;color:var(--c-ink);font-family:var(--ff-h);font-weight:700;font-size:15px;letter-spacing:-.02em;transition:border-color .2s,transform .2s,box-shadow .2s}
.villes-grid a:hover{border-color:var(--c-vert-br);transform:translateY(-2px);box-shadow:var(--shadow-card)}
.villes-grid a span{display:block;font-size:12.5px;color:var(--c-muted);font-weight:400;font-family:var(--ff-b);margin-top:3px}
@media(max-width:700px){.villes-grid{grid-template-columns:1fr 1fr}}
@media(max-width:460px){.villes-grid{grid-template-columns:1fr}}
</style>'''

def build_hub():
    url="https://leseclaires.fr/villes"
    desc=("Bornes de recharge par ville : nos guides locaux IRVE en France. Aides, prix, "
          "installateurs certifiés et simulateur gratuit, ville par ville.")
    # regrouper par région
    bygroup={}
    for sl,lb in ALL_CITIES: bygroup.setdefault(REGION[sl],[]).append((sl,lb))
    sections=''
    item_ld=[]; pos=0
    for reg in REGION_ORDER:
        if reg not in bygroup: continue
        cards=''
        for sl,lb in sorted(bygroup[reg], key=lambda x:x[1]):
            pos+=1
            item_ld.append({"@type":"ListItem","position":pos,"name":f"Borne de recharge {lb}",
                            "url":f"https://leseclaires.fr/villes/borne-recharge-{sl}.html"})
            cards+=f'      <a href="/villes/borne-recharge-{sl}.html">Borne de recharge {lb}<span>{reg} · {CODE[sl]}</span></a>\n'
        sections+=f'  <div class="villes-region">\n    <h2>{reg}</h2>\n    <div class="villes-grid">\n{cards}    </div>\n  </div>\n\n'
    graph={"@context":"https://schema.org","@graph":[
      {"@type":"CollectionPage","name":"Bornes de recharge par ville","description":desc,"url":url},
      {"@type":"ItemList","itemListElement":item_ld},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Accueil","item":"https://leseclaires.fr/"},
        {"@type":"ListItem","position":2,"name":"Bornes par ville","item":url}]},
    ]}
    jsonld='<script type="application/ld+json">\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n</script>'
    html=f'''<!DOCTYPE html>
<html lang="fr">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bornes de recharge par ville : nos guides locaux IRVE | Les Éclairés</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="borne de recharge par ville, IRVE par ville, installation borne ville, guide local borne recharge">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Bornes de recharge par ville | Les Éclairés">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://leseclaires.fr/nous-les-eclaires.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bornes de recharge par ville | Les Éclairés">
<meta name="twitter:description" content="{desc}">
{FAVICON}
{FONTS}
{jsonld}
{CSS}
{EXTRA_CSS}
{HUB_CSS}
<noscript><style>#preloader{{display:none!important}}</style></noscript>
</head>
<body>
{PRELOADER}
<nav>
  <a class="nav-logo" href="/"><img src="{NAVLOGO}" alt="Les Éclairés"><span>Les Éclairés</span></a>
  <a class="btn-nav" href="/simulateur">Simuler mon projet</a>
</nav>

<div class="hero-city">
  <div class="breadcrumb"><a href="/">Accueil</a> › <span>Bornes par ville</span></div>
  <div class="city-badge"><span class="badge-dot"></span>Guides locaux IRVE · France entière</div>
  <h1 class="city-h1">Bornes de recharge,<br><span style="white-space:nowrap">ville par ville</span></h1>
  <p class="city-sub">Aides locales, prix constatés, installateurs certifiés IRVE et délais : retrouvez nos guides dédiés à votre ville. Et où que vous soyez en France, le simulateur vous donne une recommandation personnalisée en quelques minutes.</p>
  <a href="/simulateur" class="btn-primary">Démarrer le simulateur gratuit {ARROW}</a>
</div>

<div class="city-body">
{sections}  <div class="cta-box">
    <h3>Votre ville n'est pas listée ?</h3>
    <p>Pas d'inquiétude : on couvre toute la France. Lancez le simulateur, on vous met en relation avec un installateur certifié près de chez vous.</p>
    <a href="/simulateur" class="btn-vert">Démarrer le simulateur {ARROW}</a>
  </div>
</div>

{footer()}
  <script src="/cursor.js" defer></script>
</body>
</html>
'''
    open('villes.html','w',encoding='utf-8').write(html)
    return len(html)

if __name__ == '__main__':
    total = 0
    for c in CITIES:
        build_city(c); total += 1
    n = build_hub()
    print(f"{total} pages villes générées + hub /villes ({n} o).")
