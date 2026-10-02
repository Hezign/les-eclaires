#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contenu des pages légales (source de vérité) : mentions légales, politique de
confidentialité, conditions d'utilisation (CGU, avec l'information « plateforme de
mise en relation » de l'art. L111-7 du Code de la consommation).

Écrit le texte dans la page (après le sommaire mobile), crée cgu.html depuis le
gabarit de mentions-legales.html si besoin, puis relance _legal_toc (sommaire),
_ds_shared et _typo. Idempotent. À faire relire par un juriste.

    python3 _legal_content.py
"""
import re

import _legal_toc

DATE = 'octobre 2026'
MAIL = '<a href="mailto:contact@leseclaires.fr">contact@leseclaires.fr</a>'

MENTIONS = f'''
    <h2>1. Éditeur du site</h2>
    <div class="info-box">
      <p><strong>Éditeur :</strong> Laetitia ELOI, entrepreneur individuel, exerçant sous l'enseigne « Les Éclairés »</p>
      <p><strong>Siège :</strong> 15 rue Jean-Baptiste Clément, 42000 Saint-Étienne, France</p>
      <p><strong>SIREN :</strong> 104 910 187 · <strong>SIRET :</strong> 104 910 187 00012</p>
      <p><strong>Immatriculation :</strong> RCS Saint-Étienne, le 11/05/2026</p>
      <p><strong>Code NAF / APE :</strong> 6312Z (Exploitation de portails internet)</p>
      <p><strong>TVA :</strong> non applicable, article 293 B du CGI</p>
      <p><strong>Téléphone :</strong> <a href="tel:+33637252592">06 37 25 25 92</a></p>
      <p><strong>E-mail :</strong> {MAIL}</p>
    </div>
    <h2>2. Directrice de la publication</h2>
    <p>Laetitia ELOI, en qualité de titulaire de l'entreprise individuelle éditrice.</p>
    <h2>3. Hébergement</h2>
    <div class="info-box">
      <p><strong>Hébergeur du site :</strong> Vercel Inc.</p>
      <p><strong>Adresse :</strong> 440 N Barranca Avenue #4133, Covina, CA 91723, États-Unis</p>
      <p><strong>Contact :</strong> <a href="mailto:privacy@vercel.com">privacy@vercel.com</a> · <a href="https://vercel.com" target="_blank" rel="noopener">vercel.com</a></p>
    </div>
    <p>Le nom de domaine et la messagerie électronique sont gérés par <strong>LWS (Ligne Web Services)</strong>, SAS, 10 rue Penthièvre, 75008 Paris (RCS Paris B 851 993 683). Les outils internes (automatisation, gestion de la relation partenaires) sont hébergés sur un serveur loué auprès de <strong>Hostinger International Ltd</strong>, situé en France.</p>
    <h2>4. Conception et réalisation</h2>
    <p>Site conçu et réalisé par <strong>Hezign</strong> (<a href="https://hezign.fr" target="_blank" rel="noopener">hezign.fr</a>) : design, développement et intégration.</p>
    <h2>5. Propriété intellectuelle</h2>
    <p>La structure du site, ses textes, le simulateur et son code, la charte graphique, le logo et la marque « Les Éclairés » sont la propriété exclusive de l'éditeur ou font l'objet d'une autorisation d'utilisation. Toute reproduction, représentation, adaptation ou extraction, totale ou partielle, sans autorisation écrite préalable est interdite (article L122-4 du Code de la propriété intellectuelle) et constitue une contrefaçon.</p>
    <p>Les courtes citations sont autorisées à condition de mentionner la source et de renvoyer par un lien vers la page citée.</p>
    <p><strong>Photographies :</strong> certaines illustrations proviennent de la banque d'images <a href="https://www.pexels.com/fr-fr/license/" target="_blank" rel="noopener">Pexels</a> et sont utilisées conformément à sa licence. Elles restent la propriété de leurs auteurs. Sauf mention contraire, les personnes représentées ne sont ni des installateurs partenaires ni des clients des Éclairés. La photo des fondateurs est la propriété de l'éditeur.</p>
    <h2>6. Données personnelles</h2>
    <p>Le traitement de vos données et l'usage des cookies sont décrits dans notre <a href="/confidentialite.html">politique de confidentialité</a>. Vous pouvez exercer vos droits à tout moment à {MAIL}.</p>
    <h2>7. Nature du service et responsabilité</h2>
    <p>Les Éclairés est un service d'information et de mise en relation. Les résultats du simulateur et les informations publiées (prix, aides, délais) sont indicatifs et ne constituent ni un devis ni un engagement. Les Éclairés n'est pas partie aux contrats conclus entre les utilisateurs et les installateurs, et ne réalise aucuns travaux. Le fonctionnement complet du service est décrit dans nos <a href="/cgu.html">conditions d'utilisation</a>.</p>
    <h2>8. Liens hypertextes</h2>
    <p>Le site contient des liens vers des sites tiers (organismes publics, partenaires, sources). Les Éclairés n'exerce aucun contrôle sur ces sites et n'est pas responsable de leur contenu.</p>
    <h2>9. Accessibilité</h2>
    <p>Nous travaillons à rendre le site lisible et utilisable par tous (contrastes, taille des textes, navigation au clavier). Si vous rencontrez une difficulté, écrivez-nous à {MAIL}.</p>
    <h2>10. Droit applicable</h2>
    <p>Le site et les présentes mentions sont soumis au droit français.</p>
'''

CONFIDENTIALITE = f'''
    <div class="info-box">
      <p><strong>En résumé :</strong> nous collectons uniquement les données que vous nous fournissez. Votre demande n'est transmise qu'à <strong>un seul installateur partenaire</strong>, avec votre accord. Nous ne revendons jamais vos données. Vous pouvez les faire supprimer à tout moment à {MAIL}.</p>
    </div>
    <h2>1. Responsable du traitement</h2>
    <div class="info-box">
      <p><strong>Laetitia ELOI</strong>, entrepreneur individuel (enseigne « Les Éclairés »)</p>
      <p>15 rue Jean-Baptiste Clément, 42000 Saint-Étienne · SIREN 104 910 187</p>
      <p>Contact : {MAIL}</p>
    </div>
    <h2>2. Données collectées</h2>
    <ul>
      <li><strong>Simulateur :</strong> prénom, e-mail, téléphone, département et réponses au questionnaire sur votre logement, votre véhicule et votre projet.</li>
      <li><strong>Formulaire copropriété :</strong> nom, rôle (syndic, conseil syndical, copropriétaire), nom ou adresse de la copropriété, nombre de lots, e-mail, téléphone, description du projet.</li>
      <li><strong>Candidature partenaire :</strong> prénom, nom, e-mail professionnel, téléphone, entreprise, zone d'intervention, types de projets, qualification IRVE, message.</li>
      <li><strong>Prospection des installateurs :</strong> coordonnées professionnelles d'entreprises du secteur IRVE (raison sociale, ville, téléphone, e-mail, site, qualification), issues de sources publiques (sites des entreprises, annuaires professionnels).</li>
      <li><strong>Mesure d'audience :</strong> pages vues, type d'appareil et de navigateur, provenance, uniquement si vous acceptez les cookies de mesure d'audience.</li>
    </ul>
    <p>Nous ne collectons aucune donnée sensible.</p>
    <h2>3. Finalités et bases légales</h2>
    <ul>
      <li><strong>Vous transmettre votre recommandation</strong> : exécution de votre demande.</li>
      <li><strong>Transmettre votre demande à un installateur partenaire</strong> : votre consentement, donné en cliquant sur le bouton d'envoi après une information claire. Nous conservons la date et le contenu de chaque demande comme preuve de ce consentement.</li>
      <li><strong>Étudier une candidature partenaire et préparer le contrat</strong> : mesures précontractuelles prises à votre demande.</li>
      <li><strong>Prospecter les installateurs IRVE</strong> : notre intérêt légitime à développer notre réseau. Vous pouvez vous y opposer à tout moment, sans motif.</li>
      <li><strong>Mesure d'audience</strong> : votre consentement.</li>
      <li><strong>Sécurité du site et prévention des abus</strong> : notre intérêt légitime.</li>
    </ul>
    <h2>4. Durée de conservation</h2>
    <ul>
      <li><strong>Demandes du simulateur et du formulaire copropriété</strong> : 3 ans à compter de votre dernier contact avec nous.</li>
      <li><strong>Candidatures non retenues</strong> : 3 ans à compter du dernier contact. <strong>Partenaires sous contrat</strong> : durée du contrat, puis 5 ans (prescription) et 10 ans pour les pièces comptables.</li>
      <li><strong>Prospects installateurs</strong> : 3 ans à compter du dernier contact.</li>
      <li><strong>Données de mesure d'audience</strong> : 14 mois maximum dans Google Analytics.</li>
    </ul>
    <h2>5. Destinataires et sous-traitants</h2>
    <p>Vos données ne sont <strong>jamais vendues ni louées</strong>. Elles sont accessibles à l'équipe des Éclairés et, pour les seuls besoins du service, aux destinataires suivants.</p>
    <ul>
      <li><strong>Installateur partenaire</strong> (destinataire) : un seul installateur certifié IRVE de votre secteur reçoit vos coordonnées et votre projet, uniquement si vous l'avez accepté. Il les utilise pour vous recontacter et vous faire un devis ; il devient alors responsable de ce traitement pour sa propre relation avec vous.</li>
      <li><strong>Web3Forms</strong> (acheminement des formulaires par e-mail). <a href="https://web3forms.com/privacy" target="_blank" rel="noopener">Politique ↗</a></li>
      <li><strong>Hostinger</strong> (serveur situé en France) : héberge nos outils internes d'automatisation (n8n) et de suivi des partenaires et prospects. <a href="https://www.hostinger.fr/politique-de-confidentialite" target="_blank" rel="noopener">Politique ↗</a></li>
      <li><strong>LWS</strong> (messagerie électronique et nom de domaine). <a href="https://www.lws.fr/" target="_blank" rel="noopener">Site ↗</a></li>
      <li><strong>Vercel</strong> (hébergement et diffusion du site). <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener">Politique ↗</a></li>
      <li><strong>Google Analytics 4</strong> (mesure d'audience, uniquement après votre accord). <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Politique ↗</a></li>
      <li><strong>Google Search Console</strong> (référencement) : données de recherche agrégées, sans identification des visiteurs.</li>
    </ul>
    <h2>6. Transferts hors Union européenne</h2>
    <p>Certains prestataires (notamment Google, Vercel et Web3Forms) peuvent traiter des données hors de l'Union européenne, en particulier aux États-Unis. Ces transferts sont encadrés par l'adhésion au Data Privacy Framework UE-États-Unis et/ou par les clauses contractuelles types de la Commission européenne.</p>
    <h2>7. Sécurité</h2>
    <p>Le site est servi exclusivement en HTTPS. Les accès à nos outils internes sont protégés et réservés à l'équipe. La base de suivi des partenaires et des prospects est chiffrée.</p>
    <h2>8. Vos droits</h2>
    <p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, de portabilité et d'opposition, ainsi que du droit de retirer votre consentement à tout moment (sans remettre en cause les traitements déjà réalisés). Pour les exercer : {MAIL}. Réponse sous un mois.</p>
    <p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez saisir la CNIL : <a href="https://www.cnil.fr" target="_blank" rel="noopener">cnil.fr</a>.</p>
    <h2>9. Installateurs : si nous vous avons contacté</h2>
    <p>Si vous êtes un professionnel de l'IRVE et que nous vous avons contacté, vos coordonnées professionnelles proviennent de sources publiques (site de votre entreprise, annuaires professionnels). Nous les utilisons uniquement pour vous présenter notre réseau de partenaires. Vous pouvez vous y opposer à tout moment en répondant à notre message ou à {MAIL} : vos données sont alors supprimées de nos fichiers de prospection.</p>
    <h2>10. Cookies et traceurs</h2>
    <ul>
      <li><strong>Préférences (sans consentement requis)</strong> : votre choix concernant les cookies et votre thème clair ou sombre, enregistrés dans votre navigateur.</li>
      <li><strong>Mesure d'audience (Google Analytics 4)</strong> : le script de Google n'est chargé qu'après votre accord. Les cookies _ga et _ga_* sont alors déposés pour 13 mois maximum.</li>
    </ul>
    <p>Vous pouvez modifier votre choix à tout moment avec la bulle cookies en bas de l'écran.</p>
    <h2>11. Modifications</h2>
    <p>Cette politique peut évoluer. La version en vigueur est celle publiée sur cette page, avec sa date de mise à jour.</p>
'''

CGU = f'''
    <div class="info-box">
      <p><strong>En résumé :</strong> Les Éclairés vous aide gratuitement à comprendre et cadrer votre projet de borne de recharge, puis, si vous le souhaitez, transmet votre demande à <strong>un seul installateur certifié IRVE</strong> de votre secteur. Nous sommes rémunérés par cet installateur, jamais par vous, et nous ne réalisons aucuns travaux.</p>
    </div>
    <h2>1. Objet</h2>
    <p>Les présentes conditions d'utilisation encadrent l'accès au site leseclaires.fr et l'utilisation de ses services (contenus, simulateur, mise en relation). L'utilisation du site vaut acceptation de ces conditions. L'éditeur est identifié dans les <a href="/mentions-legales.html">mentions légales</a>.</p>
    <h2>2. Les services proposés</h2>
    <ul>
      <li><strong>Information</strong> : guides, pages locales et articles sur la recharge des véhicules électriques, les aides et l'installation.</li>
      <li><strong>Simulateur</strong> : à partir de vos réponses, une recommandation indicative (puissance, budget estimatif, aides mobilisables, délai).</li>
      <li><strong>Mise en relation</strong> : si vous le demandez, la transmission de votre projet à un installateur partenaire.</li>
    </ul>
    <p>Ces services sont gratuits pour les particuliers, les copropriétés, les entreprises et les collectivités qui les utilisent.</p>
    <h2>3. Comment fonctionne la mise en relation</h2>
    <p>Cette section répond à l'obligation d'information des plateformes en ligne (article L111-7 du Code de la consommation).</p>
    <ul>
      <li><strong>Notre rôle</strong> : Les Éclairés est un service de mise en relation. Nous ne vendons aucune borne, n'avons aucun accord avec les fabricants et ne réalisons aucuns travaux.</li>
      <li><strong>Notre rémunération</strong> : l'installateur partenaire nous verse un forfait fixe pour chaque demande que nous lui transmettons, qu'un contrat soit signé ou non. Nous ne touchons aucune commission sur son devis. Le service reste gratuit pour vous.</li>
      <li><strong>Comment nous choisissons nos partenaires</strong> : nous référençons des professionnels justifiant d'une qualification IRVE en cours de validité, d'une assurance responsabilité civile professionnelle (et d'une garantie décennale selon les travaux), d'une entreprise immatriculée, et qui s'engagent à vous recontacter sous 48 h ouvrées. Un partenaire est retiré du réseau en cas de perte de sa qualification ou de manquement à ses engagements.</li>
      <li><strong>À qui va votre demande</strong> : à un seul installateur, choisi selon votre secteur géographique et le type de projet (particulier, copropriété, entreprise, collectivité). Aucun installateur ne peut payer pour être placé en priorité.</li>
      <li><strong>Votre relation avec l'installateur</strong> : vous n'êtes jamais obligé de signer. L'installateur établit librement son devis, conclut directement le contrat avec vous et reste seul responsable des travaux et de leur conformité. Les Éclairés n'est pas partie à ce contrat.</li>
    </ul>
    <h2>4. Le simulateur</h2>
    <p>Les résultats du simulateur sont des estimations établies à partir de vos réponses et des informations publiques disponibles à la date de leur mise à jour (prix constatés, barèmes d'aides). Ils sont indicatifs : ils ne constituent ni un devis, ni une offre, ni une garantie d'éligibilité à une aide. Seuls le devis de l'installateur et les décisions des organismes financeurs font foi. Les aides publiques peuvent évoluer à tout moment.</p>
    <h2>5. Transmission de votre demande</h2>
    <p>Votre demande n'est transmise qu'avec votre accord, donné en cliquant sur le bouton d'envoi après en avoir été informé. L'installateur vous recontacte en principe sous 48 h ouvrées. Le traitement de vos données est décrit dans notre <a href="/confidentialite.html">politique de confidentialité</a>.</p>
    <h2>6. Vos engagements</h2>
    <p>Vous vous engagez à fournir des informations exactes, à n'utiliser le simulateur et les formulaires que pour un projet réel, et à ne pas extraire ou réutiliser de façon automatisée ou massive les contenus du site.</p>
    <h2>7. Propriété intellectuelle</h2>
    <p>Les contenus du site sont protégés, dans les conditions décrites dans les <a href="/mentions-legales.html">mentions légales</a>. Toute reproduction non autorisée est interdite.</p>
    <h2>8. Responsabilité</h2>
    <p>Les Éclairés met tout en œuvre pour publier des informations exactes et à jour, sans pouvoir garantir leur exhaustivité. Nous ne pouvons être tenus responsables des décisions prises sur la seule base des informations du site, ni de l'exécution des prestations par les installateurs, ni d'une indisponibilité temporaire du site.</p>
    <h2>9. Modification des conditions</h2>
    <p>Ces conditions peuvent évoluer. La version applicable est celle en ligne au moment de votre utilisation du site.</p>
    <h2>10. Droit applicable et litiges</h2>
    <p>Ces conditions sont soumises au droit français. En cas de difficulté, écrivez-nous d'abord à {MAIL} pour rechercher une solution amiable.</p>
'''

PAGES = {
    'mentions-legales.html': MENTIONS,
    'confidentialite.html': CONFIDENTIALITE,
    'cgu.html': CGU,
}


def ensure_cgu():
    try:
        open('cgu.html', encoding='utf-8').close()
        return
    except FileNotFoundError:
        pass
    s = open('mentions-legales.html', encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', "<title>Conditions d'utilisation Les Éclairés</title>", s, count=1)
    s = s.replace('https://leseclaires.fr/mentions-legales.html', 'https://leseclaires.fr/cgu.html')
    s = re.sub(r'<meta name="description" content="[^"]*">',
               "<meta name=\"description\" content=\"Conditions d'utilisation du site Les Éclairés : simulateur, mise en relation avec un installateur IRVE, rémunération et sélection des partenaires.\">", s, count=1)
    s = s.replace('<div class="page-tag">Légal</div>', '<div class="page-tag">Conditions</div>', 1)
    s = s.replace('<h1>Mentions légales</h1>', "<h1>Conditions d'utilisation</h1>", 1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', "<meta property=\"og:title\" content=\"Conditions d'utilisation Les Éclairés\">", s)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="https://leseclaires.fr/cgu.html">', s)
    open('cgu.html', 'w', encoding='utf-8').write(s)


def write(path, prose):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<div class="prose">)(.*?)(\n\s*</div>(?:<!--/legal-layout--></div>)?\n</div>\n<footer)', s, re.S)
    if not m:
        raise SystemExit(f'structure inattendue : {path}')
    s = s[:m.start(2)] + prose + s[m.start(3):]
    s = re.sub(r'(<p class="page-date">Dernière mise à jour[\s\u00a0]*:[\s\u00a0]*)[^<]*', r'\g<1>' + DATE, s, count=1)
    open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    ensure_cgu()
    for p, prose in PAGES.items():
        write(p, prose)
        _legal_toc.build(p)
    import _ds_shared, _typo
    for p in PAGES:
        _ds_shared.apply(p)
        _typo.apply(p)
    print('pages légales écrites :', ', '.join(PAGES))
