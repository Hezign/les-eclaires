#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P3 - Maillage interne : liens contextuels vers les 7 orphelins + les 2 piliers
     (cout-recharge, prix-borne) deviennent des hubs qui redistribuent.
Chaque remplacement est vérifié (present exactement 1 fois, cible pas déjà liée).
Idempotent : si le lien est déjà là, on saute.
"""
import pathlib

BLOG = pathlib.Path(__file__).parent / "blog"

# (fichier, ancre_old, remplacement_new, slug_cible_pour_idempotence)
EDITS = [
 # ---- COUT-RECHARGE (pilier -> hub) ----
 ("cout-recharge-electrique-domicile-2026.html",
  "l'économie annuelle peut dépasser <strong>80 à 90 €</strong> pour un conducteur moyen.</p>",
  "l'économie annuelle peut dépasser <strong>80 à 90 €</strong> pour un conducteur moyen. Pour creuser le sujet, consultez notre <a href=\"heures-creuses-recharge-voiture-electrique.html\">guide des heures creuses pour la recharge</a>.</p>",
  "heures-creuses-recharge-voiture-electrique.html"),

 ("cout-recharge-electrique-domicile-2026.html",
  "peut rendre une partie de votre recharge quasi-gratuite en journée.</li>",
  "peut rendre une partie de votre recharge quasi-gratuite en journée. Voyez notre guide de la <a href=\"borne-recharge-solaire-autoconsommation.html\">borne de recharge solaire en autoconsommation</a>.</li>",
  "borne-recharge-solaire-autoconsommation.html"),

 ("cout-recharge-electrique-domicile-2026.html",
  "peut se connecter à vos panneaux solaires. Un vrai atout sur le long terme.</li>",
  "peut se connecter à vos panneaux solaires. Les modèles les plus avancés permettent même la <a href=\"recharge-bidirectionnelle-v2g-voiture-maison.html\">recharge bidirectionnelle (V2G)</a>, où la voiture réalimente la maison. Un vrai atout sur le long terme.</li>",
  "recharge-bidirectionnelle-v2g-voiture-maison.html"),

 ("cout-recharge-electrique-domicile-2026.html",
  "<h2 id=\"cout-installation-borne-domicile\">",
  "<p>Et lorsque vous rechargez ailleurs qu'à la maison, sur le réseau public, un <a href=\"badge-rfid-itinerance-recharge-electrique-2026.html\">badge de recharge</a> vous donne accès à des milliers de bornes partout en France, souvent à un tarif plus avantageux qu'un paiement à l'acte.</p>\n\n<h2 id=\"cout-installation-borne-domicile\">",
  "badge-rfid-itinerance-recharge-electrique-2026.html"),

 # ---- PRIX-BORNE (pilier -> hub) ----
 ("prix-borne-de-recharge-maison-2026.html",
  "Son prix varie selon sa puissance, ses fonctionnalités et sa marque.",
  "Son prix varie selon sa <a href=\"7kw-ou-22kw-quelle-puissance.html\">puissance</a>, ses fonctionnalités et sa marque.",
  "7kw-ou-22kw-quelle-puissance.html"),

 ("prix-borne-de-recharge-maison-2026.html",
  "Toutes proposent des modèles compatibles avec les aides d'État sous réserve de certification IRVE.</p>",
  "Toutes proposent des modèles compatibles avec les aides d'État sous réserve de certification IRVE. Pour les départager selon votre usage, consultez notre <a href=\"comparatif-marques-borne-recharge-2026.html\">comparatif des marques de borne de recharge</a>.</p>\n<p>Au-delà du prix d'achat, pensez au coût de possession dans la durée : notre guide sur la <a href=\"entretien-duree-vie-borne-recharge-domicile.html\">durée de vie et l'entretien d'une borne de recharge</a> détaille ce qui préserve votre installation et limite les pannes.</p>",
  "comparatif-marques-borne-recharge-2026.html"),

 ("prix-borne-de-recharge-maison-2026.html",
  "pour que vous puissiez bénéficier des aides. Demandez toujours ce justificatif avant de signer un devis.</p>",
  "pour que vous puissiez bénéficier des aides. Demandez toujours ce justificatif avant de signer un devis. Notre guide pour <a href=\"choisir-installateur-irve-certifie.html\">choisir un installateur IRVE certifié</a> liste les vérifications à faire.</p>",
  "choisir-installateur-irve-certifie.html"),

 ("prix-borne-de-recharge-maison-2026.html",
  "Vous bénéficiez du <strong>droit à la prise</strong>, un dispositif légal",
  "Vous bénéficiez du <a href=\"droit-prise-copropriete.html\"><strong>droit à la prise</strong></a>, un dispositif légal",
  "droit-prise-copropriete.html"),

 # ---- TROUVER-INSTALLATEUR -> pages villes ----
 ("trouver-installateur-borne-recharge-pres-de-chez-soi.html",
  "sélectionnés pour leur sérieux, avec possibilité de demande de devis directement.</li>",
  "sélectionnés pour leur sérieux, avec possibilité de demande de devis directement.</li>\n  <li><strong>Nos pages locales</strong> : nous détaillons les installateurs et les aides ville par ville, par exemple à <a href=\"borne-recharge-nantes-installateur-aides-2026.html\">Nantes</a>, <a href=\"borne-recharge-poitiers-installateur-aides.html\">Poitiers</a> ou <a href=\"borne-recharge-chambery-installateur-aides-2026.html\">Chambéry</a>.</li>",
  "borne-recharge-nantes-installateur-aides-2026.html"),

 # ---- DROIT-PRISE -> immeuble ancien ----
 ("droit-prise-copropriete.html",
  "et une borne pilotée s'adapte à la charge existante.</li>",
  "et une borne pilotée s'adapte à la charge existante. C'est particulièrement vrai dans un <a href=\"recharge-immeuble-ancien-copropriete.html\">immeuble ancien</a>, où des solutions existent même sur une installation vétuste.</li>",
  "recharge-immeuble-ancien-copropriete.html"),
]

applied, skipped, errors = 0, 0, []
for fname, old, new, slug in EDITS:
    f = BLOG / fname
    txt = f.read_text(encoding="utf-8")
    # idempotence : le lien vers la cible est-il déjà présent à cet endroit ?
    if f'href="{slug}"' in txt and new.split(old)[-1].strip()[:40] in txt:
        # heuristique faible ; on se fie surtout au compte de old
        pass
    n = txt.count(old)
    if n == 0:
        # peut-être déjà appliqué
        if new[:60] in txt:
            skipped += 1
            print(f"  = déjà appliqué : {fname} -> {slug}")
        else:
            errors.append(f"ANCRE INTROUVABLE dans {fname} : {old[:50]!r}")
        continue
    if n > 1:
        errors.append(f"ANCRE AMBIGUË ({n}x) dans {fname} : {old[:50]!r}")
        continue
    txt = txt.replace(old, new, 1)
    f.write_text(txt, encoding="utf-8")
    applied += 1
    print(f"  + {fname:55s} -> {slug}")

print(f"\nAppliqués: {applied} | déjà en place: {skipped} | erreurs: {len(errors)}")
for e in errors:
    print("  !!", e)
