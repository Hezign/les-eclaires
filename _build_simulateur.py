#!/usr/bin/env python3
# Génère simulateur.html à partir des blocs réutilisés de index.html (même D.A.)
import re

src = open('index.html', encoding='utf-8').read()

def between(a, b, s, inclusive=True):
    i = s.index(a)
    j = s.index(b, i + len(a))
    return s[i:j+len(b)] if inclusive else s[i+len(a):j]

# --- CSS principal (intégral) ---
css = between('<style>', '</style>', src)

# --- Liens polices ---
fonts = between('<link rel="preconnect" href="https://fonts.googleapis.com">',
                'rel="stylesheet">', src)

# --- Favicon (réutilise l'icône base64 de la home) ---
favicon = between('<link rel="icon"', '>', src) + '\n' + \
          between('<link rel="apple-touch-icon"', '>', src)

# --- NAV (on adapte les ancres vers la home) ---
nav = between('<nav>', '</nav>', src)
nav = nav.replace('href="#pourquoi"', 'href="/#pourquoi"')
nav = nav.replace('href="#histoire"', 'href="/#histoire"')
nav = nav.replace('href="#partenaires"', 'href="/partenaires.html"')
nav = nav.replace('href="#faq"', 'href="#faq"')                # FAQ locale
nav = nav.replace('href="#simulateur-start"', 'href="#simulateur-start"')  # local
nav = nav.replace('<a class="nav-logo" href="#">', '<a class="nav-logo" href="/">')

# --- Section simulateur (intégrale) ---
sim = between('<section class="sim-section" id="simulateur">', '</section>', src)

# --- Footer (intégral) ---
footer = between('<footer>', '</footer>', src)

# --- Script principal (DATA + pick/showResult/submitForm + init) ---
main_js = between('<script>\n!function(){', '}();\n</script>', src)
main_js = '<script>\n!function(){' + main_js[len('<script>\n!function(){'):]

# --- Script Web3Forms (envoi du rapport détaillé) ---
# Du <script> précédant "var KEY=" jusqu'au </script> qui suit.
k = src.index("var KEY='1109c206")
s_open = src.rindex('<script>', 0, k)
s_close = src.index('</script>', k) + len('</script>')
report_js = src[s_open:s_close]

# Cookie + back-to-top (petits blocs, réécrits)
cookie = '''<div class="cookie-banner" id="cookieBanner">
  <p>&#x1F36A; <strong>Cookies</strong> : On utilise des cookies pour analyser l'audience et améliorer votre expérience. Aucune donnée n'est revendue à des tiers.</p>
  <div class="cookie-btns">
    <button class="cookie-accept" id="btnAccept">Accepter</button>
    <button class="cookie-decline" id="btnDecline">Refuser</button>
  </div>
</div>'''

btt = '''<button class="btt" id="btt" aria-label="Retour en haut">
  <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>
</button>'''

# ---- CSS additionnel propre à la page ----
page_css = '''
<style>
/* ===== Page Simulateur (spécifique) ===== */
.simp-hero{position:relative;padding:120px 0 40px;border-bottom:1px solid var(--c-border);overflow:hidden}
.simp-hero .sw{position:relative;z-index:2}
.simp-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 14px 5px 8px;background:var(--c-vert-bg);border:1px solid var(--c-vert-br);border-radius:var(--r-full);font-size:12.5px;font-weight:500;color:var(--c-vert);margin-bottom:22px}
.simp-badge .badge-dot{width:6px;height:6px;background:var(--c-vert);border-radius:50%}
.simp-hero h1{font-size:clamp(34px,5vw,62px);font-weight:800;letter-spacing:-.045em;line-height:1.06;color:var(--c-ink);max-width:760px;margin:0 0 20px}
.simp-hero h1 .hl{color:var(--c-vert)}
.simp-hero .lead{font-size:18px;font-weight:300;line-height:1.7;color:var(--c-mid);max-width:600px;margin:0 0 28px}
.simp-points{display:flex;flex-wrap:wrap;gap:10px 22px;margin:0 0 8px;padding:0;list-style:none}
.simp-points li{display:inline-flex;align-items:center;gap:8px;font-size:14.5px;font-weight:500;color:var(--c-text)}
.simp-points svg{width:18px;height:18px;color:var(--c-vert);flex-shrink:0}

/* Comment ça marche */
.simp-steps{padding:80px 0}
.simp-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:48px}
.simp-step{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-xl);padding:28px 24px;box-shadow:var(--shadow-card);transition:transform .28s var(--ease-out),box-shadow .28s,border-color .28s}
.simp-step:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--c-vert-br)}
.simp-step-n{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:var(--r-md);background:var(--c-vert-bg);color:var(--c-vert);font-family:var(--ff-h);font-weight:800;font-size:17px;margin-bottom:16px}
.simp-step h3{font-size:17px;font-weight:700;letter-spacing:-.03em;margin:0 0 8px;color:var(--c-ink)}
.simp-step p{font-size:14px;line-height:1.65;color:var(--c-muted);font-weight:300;margin:0}

/* Bandeau confiance */
.simp-trust{padding:0 0 80px}
.simp-trust-box{background:var(--c-ink);border-radius:var(--r-xl);padding:44px 40px;display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.simp-trust-item .n{font-family:var(--ff-h);font-size:40px;font-weight:800;letter-spacing:-.05em;color:var(--c-vert-lt);line-height:1;margin-bottom:8px}
.simp-trust-item p{font-size:14px;line-height:1.6;color:rgba(255,255,255,.72);margin:0;font-weight:300}

@media(max-width:860px){
  .simp-grid{grid-template-columns:1fr 1fr}
  .simp-trust-box{grid-template-columns:1fr;gap:24px;padding:32px 26px}
}
@media(max-width:520px){
  .simp-grid{grid-template-columns:1fr}
}
</style>'''

# ---- Hero d'intro (contenu unique) ----
hero = '''<section class="simp-hero">
  <div class="hero-grain" aria-hidden="true"></div>
  <div class="sw">
    <div class="simp-badge"><span class="badge-dot"></span>Gratuit · Sans inscription · Résultat immédiat</div>
    <h1>Simulateur IRVE&nbsp;: votre projet de <span class="hl">borne de recharge</span>, clair en 3 minutes.</h1>
    <p class="lead">Répondez à 8 questions simples. On vous dit exactement quelle borne installer, combien ça coûte vraiment, les aides auxquelles vous avez droit et le délai d'installation. Sans jargon, sans engagement.</p>
    <ul class="simp-points">
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>Recommandation personnalisée</li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>Budget &amp; aides estimés</li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>Installateur certifié près de chez vous</li>
    </ul>
  </div>
</section>'''

# ---- Comment ça marche (contenu unique) ----
steps = '''<section class="simp-steps">
  <div class="sw">
    <div class="reveal">
      <span class="section-tag">Comment ça marche</span>
      <h2 class="section-h2">De vos réponses à votre borne, en 4 étapes</h2>
      <p class="section-lead">Un parcours pensé pour aller droit au but, sans démarche compliquée.</p>
    </div>
    <div class="simp-grid">
      <div class="simp-step reveal">
        <div class="simp-step-n">1</div>
        <h3>Vous répondez</h3>
        <p>8 questions sur votre logement, votre véhicule et vos habitudes de recharge. Trois minutes, montre en main.</p>
      </div>
      <div class="simp-step reveal">
        <div class="simp-step-n">2</div>
        <h3>On analyse</h3>
        <p>Notre moteur croise vos réponses pour déterminer la puissance, le budget réaliste et les aides mobilisables.</p>
      </div>
      <div class="simp-step reveal">
        <div class="simp-step-n">3</div>
        <h3>Vous recevez votre reco</h3>
        <p>Un récapitulatif détaillé de votre projet, clair et neutre, envoyé directement par email.</p>
      </div>
      <div class="simp-step reveal">
        <div class="simp-step-n">4</div>
        <h3>On vous met en relation</h3>
        <p>Avec un installateur certifié IRVE sélectionné pour votre projet. Vous décidez librement, sans engagement.</p>
      </div>
    </div>
  </div>
</section>'''

# ---- Bandeau confiance ----
trust = '''<section class="simp-trust">
  <div class="sw">
    <div class="simp-trust-box reveal">
      <div class="simp-trust-item"><div class="n">100 %</div><p>Gratuit pour les particuliers, sans aucune inscription.</p></div>
      <div class="simp-trust-item"><div class="n">3 min</div><p>Pour obtenir une recommandation complète et personnalisée.</p></div>
      <div class="simp-trust-item"><div class="n">0</div><p>Conflit d'intérêts : on ne vend aucune borne, nos conseils sont neutres.</p></div>
    </div>
  </div>
</section>'''

# ---- FAQ propre au simulateur (contenu unique) ----
faq_items = [
 ("Le simulateur est-il vraiment gratuit ?",
  "Oui, totalement. Le simulateur et la recommandation sont 100&nbsp;% gratuits pour les particuliers, sans inscription ni carte bancaire. Notre modèle repose sur une commission versée par l'installateur lors de la mise en relation&nbsp;: cela ne change rien à votre prix."),
 ("Combien de temps prend la simulation ?",
  "Environ 3 minutes. Ce sont 8 questions simples sur votre logement, votre véhicule et vos habitudes. Aucune connaissance technique n'est nécessaire&nbsp;: on traduit tout en langage clair."),
 ("Dois-je créer un compte ?",
  "Non. Vous répondez aux questions directement, et vous renseignez seulement votre email (et éventuellement votre téléphone) à la fin pour recevoir votre récapitulatif détaillé."),
 ("Que se passe-t-il après la simulation ?",
  "Vous recevez par email un récapitulatif complet de votre projet&nbsp;: puissance conseillée, budget estimé, aides mobilisables et délai. Ensuite, on vous met en relation avec un installateur certifié IRVE sélectionné pour votre situation, sous 24&nbsp;à 48&nbsp;heures."),
 ("Les résultats sont-ils fiables ?",
  "Les estimations s'appuient sur des fourchettes réelles du marché (matériel, pose, aides en vigueur). Elles donnent une vision juste de votre projet. Le devis final est ensuite confirmé par l'installateur après étude de votre installation électrique."),
 ("Mes données sont-elles protégées ?",
  "Oui. Vos informations servent uniquement à établir votre recommandation et la mise en relation avec un installateur. Aucune donnée n'est revendue à des tiers. Voir notre <a href=\"/confidentialite.html\" style=\"color:var(--c-vert);font-weight:600;text-decoration:none\">politique de confidentialité</a>."),
]
faq_html = '\n'.join(
 f'''      <div class="faq-item">
        <button class="faq-q" onclick="toggleFaq(this)">
          <span>{q}</span>
          <svg class="faq-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="faq-a"><p>{a}</p></div>
      </div>''' for q, a in faq_items)

faq = f'''<section class="faq-section" id="faq">
  <div class="sw">
    <div class="reveal">
      <span class="section-tag">Questions fréquentes</span>
      <h2 class="section-h2">Tout savoir sur le simulateur</h2>
      <p class="section-lead">Les réponses aux questions qu'on nous pose le plus souvent.</p>
    </div>
    <div class="faq-grid reveal">
{faq_html}
    </div>
  </div>
</section>'''

# ---- JSON-LD ----
faq_ld = ',\n'.join(
 '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (
   __import__('json').dumps(q, ensure_ascii=False),
   __import__('json').dumps(re.sub('<[^>]+>','',a).replace('\xa0',' '), ensure_ascii=False)
 ) for q, a in faq_items)

jsonld = '''<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@graph":[
    {
      "@type":"WebApplication",
      "name":"Simulateur IRVE — Les Éclairés",
      "url":"https://leseclaires.fr/simulateur",
      "applicationCategory":"UtilityApplication",
      "operatingSystem":"Web",
      "offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},
      "description":"Simulateur gratuit pour choisir et installer une borne de recharge (IRVE) en France : puissance, budget, aides ADVENIR et délai en 3 minutes."
    },
    {
      "@type":"BreadcrumbList",
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Accueil","item":"https://leseclaires.fr/"},
        {"@type":"ListItem","position":2,"name":"Simulateur","item":"https://leseclaires.fr/simulateur"}
      ]
    },
    {
      "@type":"FAQPage",
      "mainEntity":[''' + faq_ld + ''']
    }
  ]
}
</script>'''

# ===== Assemblage =====
html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simulateur IRVE gratuit — Borne de recharge en 3 min | Les Éclairés</title>
<meta name="description" content="Simulateur IRVE gratuit : trouvez la bonne borne de recharge en 3 minutes. Puissance, budget, aides ADVENIR et délai. Sans inscription, guide indépendant.">
<meta name="keywords" content="simulateur IRVE, simulateur borne de recharge, borne recharge gratuit, prime ADVENIR, puissance borne, installateur IRVE">
<link rel="canonical" href="https://leseclaires.fr/simulateur">
<meta name="robots" content="index,follow,max-image-preview:large">

<meta property="og:type" content="website">
<meta property="og:url" content="https://leseclaires.fr/simulateur">
<meta property="og:title" content="Simulateur IRVE gratuit — Borne de recharge en 3 min | Les Éclairés">
<meta property="og:description" content="Trouvez la bonne borne de recharge en 3 minutes : puissance, budget, aides et délai. Gratuit, sans inscription.">
<meta property="og:image" content="https://leseclaires.fr/nous-les-eclaires.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Simulateur IRVE gratuit — Les Éclairés">
<meta name="twitter:description" content="Trouvez la bonne borne de recharge en 3 minutes : puissance, budget, aides et délai.">

{favicon}
{fonts}
{jsonld}
{css}
{page_css}
</head>
<body>

{nav}

<main>
{hero}

{sim}

{steps}

{trust}

{faq}
</main>

{footer}

{cookie}

{btt}

{main_js}

{report_js}
</body>
</html>
'''

open('simulateur.html', 'w', encoding='utf-8').write(html)
print("simulateur.html écrit :", len(html), "octets")
# sanity
for tag in ['id="simulateur-start"','function pick','var KEY=','faq-q','simp-hero']:
    print(' -', tag, 'présent' if tag in html else 'MANQUANT')
