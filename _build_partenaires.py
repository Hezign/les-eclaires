"""Page « Devenir partenaire » (partenaires.html) : contenu B2B installateurs.
Idempotent : remplace le corps entre <div class="page"> (ou le bloc partenaire déjà
posé) et la section « Ressources installateurs », garde header/footer/formulaire JS.

Tout le contenu reflète le contrat partenaire (contrat-partenaire-irve.md) :
1 demande = 1 seul installateur (art. 3.2/6.1), transmission sous 24 h (3.3),
rappel client sous 48 h ouvrées (3.4), forfait fixe par demande indépendant de la
signature (2, 7.2), facture mensuelle à 30 jours (7.3/7.4), aucun volume minimum
(7.6), toute demande transmise est due, sans remboursement (8, décision Harry 02/10/2026), contrat 12 mois préavis 30 j (9).
La grille de prix n'est PAS publiée (décision Harry 01/10/2026) : « sur demande ».

    python3 _build_partenaires.py
"""
import json
import re

PATH = 'partenaires.html'

TITLE = 'Devenir partenaire installateur IRVE | Les Éclairés'
DESC = ("Installateur IRVE : recevez des demandes de pose qualifiées et exclusives "
        "sur votre zone. Sans abonnement ni volume minimum, payées à la demande.")

ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M3 8h10M9 4l4 4-4 4"/></svg>')
CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')

FAQ = [
    ("Combien coûte une demande ?",
     "Un forfait fixe par demande, qui dépend du type de projet (particulier, entreprise, "
     "copropriété, collectivité). Pas d'abonnement, pas de commission sur vos chantiers. "
     "La grille complète vous est présentée lors du premier échange."),
    ("La même demande est-elle envoyée à d'autres installateurs ?",
     "Non. Chaque demande n'est transmise qu'à un seul installateur partenaire. "
     "Plusieurs partenaires peuvent couvrir une même zone, mais un client donné n'est "
     "adressé qu'à l'un d'entre eux."),
    ("Suis-je engagé sur un volume ?",
     "Non. Vous ne payez que les demandes valides reçues dans le mois, sans minimum. "
     "En contrepartie, nous ne garantissons pas de volume. Le contrat partenaire est "
     "conclu pour 12 mois et se résilie avec 30 jours de préavis avant l'échéance."),
    ("Quelles demandes me sont transmises ?",
     "Uniquement des demandes situées dans votre zone, sur les types de projets que vous traitez, "
     "avec les coordonnées du client et son accord pour être recontacté. Une même demande ne vous "
     "est jamais transmise deux fois. Toute demande transmise est due, quelle que soit sa suite."),
    ("Les Éclairés intervient-il dans mes devis ou mes chantiers ?",
     "Non. Vous fixez vos prix, établissez votre devis et réalisez l'installation. "
     "Notre rôle s'arrête à la transmission de la demande qualifiée."),
    ("Faut-il être qualifié IRVE ?",
     "Oui. La qualification IRVE est obligatoire pour installer une borne de recharge de plus "
     "de 3,7 kW, et c'est une condition pour rejoindre le réseau. Si vous êtes en cours de "
     "qualification, indiquez-le dans votre candidature."),
]

CSS = '''<style id="partner-css">
.pt-wrap{max-width:1080px;margin:0 auto;padding:0 48px}
.pt-hero{padding:150px 0 72px}
.pt-hero .page-title{max-width:760px;font-size:clamp(34px,5vw,58px);line-height:1.04;margin-bottom:20px}
.pt-hero .page-sub{max-width:640px;margin-bottom:32px;font-size:17px}
.pt-ctas{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:36px}
.pt-btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--ff-h);font-weight:700;font-size:15px;letter-spacing:-.02em;padding:14px 26px;border-radius:var(--r-full);transition:transform .18s var(--ease-spring),background .2s,border-color .2s}
.pt-btn:hover{transform:translateY(-2px)}
.pt-btn-main{background:var(--c-vert-lt);color:#000}
.pt-btn-ghost{border:1px solid var(--c-border2);color:var(--c-ink)}
.pt-btn-ghost:hover{border-color:var(--c-ink)}
.pt-chips{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}
.pt-chips li{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600;color:var(--c-ink);background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-full);padding:8px 16px}
.pt-chips svg{width:15px;height:15px;color:var(--c-vert-txt)}
.pt-sec{padding:88px 0}
.pt-sec.alt{background:var(--c-bg2);border-top:1px solid var(--c-border);border-bottom:1px solid var(--c-border)}
.pt-sec.menthe{background:var(--c-menthe)}
.pt-sec.band{background:var(--c-band);color:rgba(255,255,255,.78)}
.pt-kicker{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-vert-txt);margin-bottom:14px}
.pt-sec.band .pt-kicker{color:var(--c-vert-lt)}
.pt-h2{font-family:var(--ff-h);font-size:clamp(28px,3.6vw,42px);font-weight:800;letter-spacing:-.035em;line-height:1.1;color:var(--c-ink);margin:0 0 14px;max-width:720px}
.pt-sec.band .pt-h2{color:#fff}
.pt-lead{font-size:16.5px;color:var(--c-mid);line-height:1.75;max-width:680px;margin:0 0 40px}
.pt-sec.band .pt-lead{color:rgba(255,255,255,.72)}
.pt-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.pt-card{background:var(--c-bg);border:1px solid var(--c-border);border-radius:var(--r-lg);padding:28px}
.pt-sec.alt .pt-card{background:var(--c-bg)}
.pt-card .n{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;color:var(--c-vert-txt);margin-bottom:14px;display:block}
.pt-card h3{font-size:20px;font-weight:700;letter-spacing:-.025em;margin:0 0 8px}
.pt-card p{font-size:15px;color:var(--c-mid);line-height:1.7;margin:0}
.pt-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:56px;align-items:start}
.pt-list{list-style:none;padding:0;margin:0;display:grid;gap:14px}
.pt-list li{display:flex;gap:12px;font-size:15.5px;line-height:1.6;color:var(--c-text)}
.pt-list li svg{flex:none;width:20px;height:20px;margin-top:2px;color:var(--c-vert-txt)}
.pt-sec.band .pt-list li{color:rgba(255,255,255,.86)}
.pt-sec.band .pt-list li svg{color:var(--c-vert-lt)}
.pt-roles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.pt-role{border-radius:var(--r-lg);padding:30px;border:1px solid var(--c-border)}
.pt-role.us{background:var(--c-band);color:rgba(255,255,255,.8);border-color:transparent}
.pt-role.you{background:var(--c-bg2)}
.pt-role h3{font-size:22px;font-weight:800;letter-spacing:-.03em;margin:0 0 18px}
.pt-role.us h3{color:#fff}
.pt-role.us .pt-list li{color:rgba(255,255,255,.86)}
.pt-role.us .pt-list li svg{color:var(--c-vert-lt)}
.pt-note{font-size:14px;color:var(--c-muted);margin:20px 0 0;line-height:1.6}
.pt-price{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:var(--r-lg);padding:30px}
.pt-price p{margin:0 0 20px;color:rgba(255,255,255,.78);line-height:1.7}
.pt-price strong{color:#fff}
.pt-steps{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;counter-reset:st}
.pt-steps li{background:var(--c-bg2);border:1px solid var(--c-border);border-radius:var(--r-lg);padding:26px}
.pt-steps .n{display:inline-flex;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12px;font-weight:500;color:#000;background:var(--c-vert-lt);border-radius:var(--r-full);padding:4px 10px;margin-bottom:16px}
.pt-steps h3{font-size:18px;font-weight:700;letter-spacing:-.025em;margin:0 0 8px}
.pt-steps p{font-size:14.5px;color:var(--c-mid);line-height:1.65;margin:0}
.pt-form-sec{padding:88px 0}
.pt-form-sec .form-card{max-width:820px}
.pt-faq{display:grid;gap:10px;max-width:820px}
.pt-faq details{background:var(--c-bg);border:1px solid var(--c-border);border-radius:var(--r-md)}
.pt-faq summary{cursor:pointer;list-style:none;padding:18px 22px;font-family:var(--ff-h);font-weight:700;font-size:16.5px;letter-spacing:-.02em;color:var(--c-ink);display:flex;justify-content:space-between;gap:16px}
.pt-faq summary::-webkit-details-marker{display:none}
.pt-faq summary::after{content:"+";font-size:22px;line-height:1;color:var(--c-muted);flex:none}
.pt-faq details[open] summary::after{content:"\\2212"}
.pt-faq details p{margin:0;padding:0 22px 20px;font-size:15px;color:var(--c-mid);line-height:1.7}
.pt-res{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.pt-res a{display:flex;flex-direction:column;gap:8px;background:var(--c-bg);border:1px solid var(--c-border);border-radius:var(--r-lg);padding:24px 26px;text-decoration:none;transition:border-color .2s,transform .2s}
.pt-res a:hover{border-color:var(--c-vert-br);transform:translateY(-2px)}
.pt-res strong{font-family:var(--ff-h);font-size:18px;font-weight:700;letter-spacing:-.025em;color:var(--c-ink)}
.pt-res span{font-size:14.5px;line-height:1.6;color:var(--c-mid)}
.pt-res em{font-style:normal;font-family:var(--ff-h);font-weight:700;font-size:14px;color:var(--c-vert-txt);margin-top:4px}
@media(max-width:640px){.pt-res{grid-template-columns:minmax(0,1fr)}}
.pt-sec a.pt-inline{color:var(--c-vert-txt);text-decoration:underline;text-underline-offset:3px}
@media(max-width:960px){.pt-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.pt-split{grid-template-columns:minmax(0,1fr);gap:32px}}
@media(max-width:640px){.pt-wrap{padding:0 20px}.pt-hero{padding:calc(var(--topbar-h,0px) + 100px) 0 56px}.pt-sec,.pt-form-sec{padding:64px 0}.pt-grid,.pt-roles,.pt-steps{grid-template-columns:minmax(0,1fr)}.pt-card,.pt-role,.pt-price{padding:24px}.pt-form-sec .form-card{padding:24px}}
</style>'''


RES = '''<!--partner-res-->
<section class="pt-sec">
  <div class="pt-wrap">
    <span class="pt-kicker">Ressources installateurs</span>
    <h2 class="pt-h2">Pour aller plus loin</h2>
    <p class="pt-lead">Nos guides pour les professionnels de la recharge : qualification, outils et développement de votre activité.</p>
    <div class="pt-res">
      <a href="/blog/devenir-installateur-agree-advenir.html"><strong>Devenir installateur agréé ADVENIR</strong><span>Qualification IRVE, conditions et démarches pour rendre vos chantiers éligibles.</span><em>Lire le guide →</em></a>
      <a href="/blog/choisir-installateur-irve-certifie.html"><strong>Reconnaître un installateur IRVE certifié</strong><span>Ce que vérifient les particuliers avant de signer un devis.</span><em>Lire le guide →</em></a>
      <a href="/blog/logiciel-gestion-installateur-irve.html"><strong>Quel logiciel pour un installateur IRVE&nbsp;?</strong><span>Gestion de chantier ou supervision des bornes : les fonctions à prioriser.</span><em>Lire le guide →</em></a>
      <a href="/blog/trouver-installateur-borne-recharge-pres-de-chez-soi.html"><strong>Se faire trouver par les particuliers</strong><span>Comment un client cherche un installateur de borne près de chez lui.</span><em>Lire le guide →</em></a>
    </div>
  </div>
</section>
<!--/partner-res-->'''


def li(items, dark=False):
    return ''.join(f'<li>{CHECK}<span>{t}</span></li>' for t in items)


def faq_html():
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)


def faq_ld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
    }, ensure_ascii=False)


def body(form_inner):
    import _home_sections as hs
    card = hs.reco_card("Exemple de demande reçue", "Exclusive",
        [("home", "Projet", "Maison individuelle", "Zone", "Votre secteur"),
         ("bolt", "Puissance recommandée", "Borne 7,4&nbsp;kW", "Délai souhaité", "Indiqué"),
         ("euro", "Budget et aides", "Estimés", "Accord client", "Recueilli")],
        'Transmise <b style="color:var(--c-vert-lt)">à vous seul, sous 24&nbsp;h</b>, par e-mail')
    HERO = hs.hero(badge="Réseau installateurs IRVE",
        h1="Devenir partenaire <em>installateur IRVE</em>",
        lead="Recevez des demandes de pose qualifiées sur votre zone, sans prospecter. Chaque demande vient d'un particulier, d'une copropriété, d'une entreprise ou d'une collectivité qui a déjà fait sa simulation, et elle n'est transmise qu'à vous.",
        ctas=[("#candidature", "Candidater", "primary"), ("#prerequis", "Voir les prérequis", "ghost")],
        mini=[("1", "demande = 1 seul installateur"), ("24&nbsp;h", "pour la transmission"), ("0", "abonnement")],
        card=card)
    RECEVEZ = hs.section(hs.num_cards([
        ("file", "Un projet déjà cadré", "Le client a complété notre simulateur : type de logement ou de site, puissance recommandée, budget estimatif, aides mobilisables et délai souhaité. Vous savez de quoi il retourne avant d'appeler."),
        ("shield", "Une demande exclusive", "Chaque demande n'est transmise qu'à un seul installateur. Pas de mise en concurrence avec dix autres artisans sur le même contact."),
        ("clock", "Transmise sous 24&nbsp;h", "Par e-mail, au plus tard 24 heures après la demande, avec les coordonnées du client et son accord pour être recontacté."),
        ("map", "Votre zone, vos projets", "Vous déclarez vos départements ou communes et les projets que vous traitez : particuliers, copropriétés, entreprises, collectivités."),
      ]), tone='white', tag="Ce que vous recevez", h2="Des demandes prêtes à traiter",
      lead="Pas une simple liste de contacts : un projet déjà cadré, adressé à vous seul, sur les zones et les types de chantiers que vous choisissez.")
    PREREQ = hs.section(hs.top_cards([
        ("shield", "Qualification IRVE", "", "En cours de validité, obligatoire pour poser une borne de plus de 3,7&nbsp;kW."),
        ("file", "Assurances à jour", "", "Responsabilité civile professionnelle et, selon vos travaux, garantie décennale."),
        ("building", "Entreprise immatriculée", "", "Un SIRET actif pour l'entreprise qui réalise les poses."),
        ("clock", "Réactivité", "", "Recontacter chaque client sous 48&nbsp;h ouvrées après réception de la demande."),
      ]) + '<p class="pt-note">Pas encore qualifié&nbsp;? Lisez notre guide <a class="pt-inline" href="/blog/devenir-installateur-agree-advenir.html">devenir installateur agréé ADVENIR</a>.</p>',
      tone='menthe', tag="Prérequis", h2="Qui peut rejoindre le réseau ?",
      lead="Nous recommandons nos partenaires à des particuliers et à des gestionnaires qui nous font confiance. Le réseau est donc réservé aux professionnels qualifiés.", sid="prerequis")
    ETAPES = hs.section(hs.steps([
        ("Candidature", "Le formulaire ci-dessous, en deux minutes : entreprise, zone, qualification."),
        ("Premier échange", "On vous rappelle sous 48&nbsp;h ouvrées pour préciser vos zones, vos types de projets, et vous présenter la grille tarifaire."),
        ("Contrat partenaire", "Un contrat simple fixe les règles : exclusivité de chaque demande, zone, tarifs, facturation mensuelle."),
        ("Premières demandes", "Dès que votre zone est paramétrée, les demandes vous arrivent par e-mail."),
      ]), tone='band', tag="Comment ça se passe", h2="De la candidature aux premières demandes")
    FAQ = hs.faq_section("Questions fréquentes", "Les questions des installateurs",
        'Une autre question ? Écrivez-nous à <a class="pt-inline" href="mailto:contact@leseclaires.fr">contact@leseclaires.fr</a>.', faq_html())
    return f'''<!--partner-body-->
{HERO}

{RECEVEZ}

<section class="pt-sec menthe">
  <div class="pt-wrap pt-split">
    <div>
      <span class="pt-kicker">D'où viennent les demandes</span>
      <h2 class="pt-h2">Des clients qui ont déjà fait la moitié du chemin</h2>
      <p class="pt-lead" style="margin-bottom:0">Les Éclairés est un site d'information indépendant sur la recharge à domicile, en copropriété et en entreprise. Les personnes qui nous lisent cherchent à installer une borne. À la fin de la simulation, elles reçoivent une recommandation personnalisée et peuvent demander à être mises en relation avec un installateur certifié près de chez elles.</p>
    </div>
    <ul class="pt-list">{li([
        'Un <a class="pt-inline" href="/simulateur">simulateur gratuit</a>, sans inscription, qui cadre le besoin',
        'Des guides sur les aides, le droit à la prise en copropriété et le choix de la puissance',
        'Des <a class="pt-inline" href="/villes.html">pages locales</a> dans 27 villes de France',
        "Une mise en relation uniquement avec l'accord explicite du client",
    ])}</ul>
  </div>
</section>

<section class="pt-sec">
  <div class="pt-wrap">
    <span class="pt-kicker">Partage des rôles</span>
    <h2 class="pt-h2">Nous trouvons le client, vous faites le chantier</h2>
    <p class="pt-lead">Le périmètre est clair dès le départ.</p>
    <div class="pt-roles">
      <div class="pt-role us"><h3>Les Éclairés</h3><ul class="pt-list">{li([
          'Attire et informe les porteurs de projet',
          'Qualifie la demande grâce au simulateur',
          'Recueille le consentement du client',
          'Vous transmet la demande sous 24 h',
          'Ne vous transmet que des demandes de votre zone',
      ])}</ul></div>
      <div class="pt-role you"><h3>Vous</h3><ul class="pt-list">{li([
          'Recontactez le client sous 48 h ouvrées',
          'Établissez votre devis, à vos prix',
          "Réalisez l'installation",
          'Gardez seul la relation commerciale',
      ])}</ul></div>
    </div>
    <p class="pt-note">Les Éclairés n'intervient ni dans le devis, ni dans le contrat, ni dans les travaux.</p>
  </div>
</section>

<section class="pt-sec band">
  <div class="pt-wrap pt-split">
    <div>
      <span class="pt-kicker">Tarifs</span>
      <h2 class="pt-h2">Vous payez uniquement les demandes reçues</h2>
      <p class="pt-lead" style="margin-bottom:0">Un forfait fixe par demande, selon le type de projet. Il ne dépend pas de la signature du chantier : aucune commission sur vos devis.</p>
    </div>
    <div class="pt-price">
      <ul class="pt-list" style="margin-bottom:24px">{li([
          'Une facture récapitulative à la fin du mois, payable à 30 jours',
          'Aucun abonnement, aucun volume minimum',
          'Uniquement des demandes de votre zone et de vos types de projets, jamais en double',
      ])}</ul>
      <p>La grille tarifaire vous est présentée lors du <strong>premier échange</strong>.</p>
      <a class="pt-btn pt-btn-main" href="#candidature">Demander la grille {ARROW}</a>
    </div>
  </div>
</section>

{PREREQ}

{ETAPES}

<section class="pt-form-sec pt-sec menthe" id="candidature">
  <div class="pt-wrap">
    <span class="pt-kicker">Candidature</span>
    <h2 class="pt-h2">Candidater au réseau</h2>
    <p class="pt-lead">Indiquez votre entreprise, vos zones et votre qualification. Nous revenons vers vous sous 48 h ouvrées.</p>
    <div class="form-card">{form_inner}</div>
  </div>
</section>

{FAQ}
<!--/partner-body-->
'''


QUALIF_FIELD = '''<div class="form-full">
          <label for="fq">Qualification IRVE</label>
          <select class="form-in" id="fq">
            <option value="">Sélectionner...</option>
            <option value="Qualification IRVE (Qualifelec ou AFNOR Certification)">Qualification IRVE (Qualifelec ou AFNOR Certification)</option>
            <option value="Qualification en cours d'obtention">Qualification en cours d'obtention</option>
            <option value="Pas encore de qualification IRVE">Pas encore de qualification IRVE</option>
          </select>
        </div>
        '''


def build():
    s = open(PATH, encoding='utf-8').read()
    orig = s

    # Formulaire : récupérer l'intérieur de .form-card (où qu'il soit)
    fm = re.search(r'<div class="form-card">(\s*<div id="formWrap">.*?<div class="success-wrap" id="successWrap">.*?</div>\s*</div>)', s, re.S)
    if not fm:
        raise SystemExit('formulaire introuvable')
    form_inner = fm.group(1)
    if 'id="fq"' not in form_inner:
        form_inner = form_inner.replace('<div class="form-full">\n          <label for="fm">',
                                        QUALIF_FIELD + '<div class="form-full">\n          <label for="fm">', 1)
    form_inner = form_inner.replace('placeholder="Lyon, Rhône-Alpes..."', 'placeholder="Départements ou communes : 69, 42, Lyon..."')
    form_inner = form_inner.replace('<label for="fz">Zone d\'intervention</label>', '<label for="fz">Zone d\'intervention *</label>')

    # Corps : de <div class="page"> (1re fois) ou du bloc déjà posé, jusqu'à la section Ressources
    start = s.find('<!--partner-body-->')
    if start == -1:
        start = s.find('<div class="page">')
    end = s.find('<!--partner-res-->')
    if end == -1:
        end = s.find('<section style="background:var(--c-bg2);border-top:1px solid var(--c-border)">')
    if start == -1 or end == -1 or end < start:
        raise SystemExit('structure inattendue')
    s = s[:start] + body(form_inner) + '\n' + s[end:]
    s = re.sub(r'<!--partner-res-->.*?<!--/partner-res-->', lambda m: RES, s, count=1, flags=re.S)
    s = re.sub(r'<section style="background:var\(--c-bg2\);border-top:1px solid var\(--c-border\)">.*?</section>',
               lambda m: RES, s, count=1, flags=re.S)

    # Validation + envoi de la qualification
    s = s.replace("var fp=v('fp'),fn=v('fn'),fe=v('fe'),fc=v('fc'),ft=v('ft'),fz=v('fz'),fm=v('fm');",
                  "var fp=v('fp'),fn=v('fn'),fe=v('fe'),fc=v('fc'),ft=v('ft'),fz=v('fz'),fm=v('fm'),fq=v('fq');")
    s = s.replace("[['fp',fp],['fe',fe],['fc',fc]].forEach", "[['fp',fp],['fe',fe],['fc',fc],['fz',fz]].forEach")
    s = s.replace("'Zone':fz, 'Type':ft2, 'Message':fm", "'Zone':fz, 'Type':ft2, 'Qualification IRVE':fq, 'Message':fm")

    # Métadonnées
    s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
    s = s.replace('"name":"Devenir partenaire Les Éclairés"', '"name":"Devenir partenaire installateur IRVE"')
    s = re.sub(r'("@type":"WebPage".*?"description":")[^"]*', lambda m: m.group(1) + DESC, s, count=1, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json" id="partner-faq-ld">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', f'<script type="application/ld+json" id="partner-faq-ld">{faq_ld()}</script>\n</head>', 1)

    # CSS
    s = re.sub(r'<style id="partner-css">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)

    if s != orig:
        open(PATH, 'w', encoding='utf-8').write(s)
        print('maj ', PATH)
    else:
        print('skip', PATH)


if __name__ == '__main__':
    build()
    import _typo, _ds_shared
    for f in ['partenaires.html']:
        _ds_shared.apply(f); _typo.apply(f)
