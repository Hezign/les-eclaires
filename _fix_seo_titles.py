#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correctifs SEO GA4/GSC (14/09/2026) :
  P1 - Réécriture des titles > 60 car (+ suppression suffixe de marque partout)
       Répercussion dans og:title, twitter:title et headline JSON-LD.
  P4 - Correction accents « Les Eclaires » -> « Les Éclairés » (global).
  P5 - Diagnostic longueur des meta descriptions (rapport, pas de modif auto).
Idempotent : relançable sans dégât.
"""
import re, pathlib, html

BLOG = pathlib.Path(__file__).parent / "blog"

# filename (sans .html) -> nouveau title (<=55 car, mot-clé en tête, sans suffixe marque)
TITLES = {
    "badge-rfid-itinerance-recharge-electrique-2026": "Badge de recharge : rechargez partout en France",
    "cout-recharge-electrique-domicile-2026":          "Recharge à domicile : combien ça coûte en 2026 ?",
    "prix-borne-de-recharge-maison-2026":              "Prix borne de recharge maison 2026 : le budget réel",
    "borne-recharge-solaire-autoconsommation":         "Borne de recharge solaire en autoconsommation",
    "choisir-installateur-irve-certifie":              "Installateur IRVE certifié : comment bien choisir",
    "droit-prise-copropriete":                         "Droit à la prise en copropriété : procédure 2026",
    "entretien-duree-vie-borne-recharge-domicile":     "Durée de vie d'une borne de recharge : entretien",
    "guide-prime-advenir-2026":                        "Prime ADVENIR 2026 : montants, conditions, démarches",
    "installation-borne-recharge-locataire":           "Installation borne de recharge locataire : vos droits",
    "prise-renforcee-ou-borne-de-recharge":            "Prise renforcée ou borne de recharge : que choisir ?",
    "recharge-bidirectionnelle-v2g-voiture-maison":    "Recharge bidirectionnelle V2G : voiture vers maison",
    "recharge-immeuble-ancien-copropriete":            "Recharge en immeuble ancien : solutions et démarches",
    # <60 mais suffixe de marque à retirer (cohérence)
    "7kw-ou-22kw-quelle-puissance":                    "7,4 kW ou 22 kW : quelle puissance choisir ?",
    "aides-regionales-borne-recharge-2026":            "Aides régionales borne de recharge 2026",
}

def esc_html(s):  # pour attributs HTML/title
    return html.escape(s, quote=True)

def esc_json(s):  # pour valeur JSON
    return s.replace("\\", "\\\\").replace('"', '\\"')

changed = []
meta_report = []

for f in sorted(BLOG.glob("*.html")):
    if f.name in ("index.html", "template.html"):
        continue
    stem = f.stem
    txt = f.read_text(encoding="utf-8")
    orig = txt

    new_title = TITLES.get(stem)
    if new_title:
        th = esc_html(new_title)
        # <title>
        txt = re.sub(r"<title>.*?</title>", f"<title>{th}</title>", txt, count=1, flags=re.S)
        # og:title (si présent)
        txt = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*(")',
                     lambda m: m.group(1) + th + m.group(2), txt)
        # twitter:title (si présent)
        txt = re.sub(r'(<meta[^>]*name="twitter:title"[^>]*content=")[^"]*(")',
                     lambda m: m.group(1) + th + m.group(2), txt)
        # headline JSON-LD (si présent)
        txt = re.sub(r'("headline":")(?:[^"\\]|\\.)*(")',
                     lambda m: m.group(1) + esc_json(new_title) + m.group(2), txt)

    # P4 : accents marque (hors URL leseclaires.fr qui n'a pas d'espace)
    txt = txt.replace("Les Eclaires", "Les Éclairés")

    # P5 : diagnostic meta description
    md = re.search(r'<meta name="description" content="([^"]*)"', txt)
    if md:
        L = len(md.group(1))
        if L > 155:
            meta_report.append((L, f.name))

    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        changed.append(f.name)

print("=== FICHIERS MODIFIÉS ({}) ===".format(len(changed)))
for c in sorted(changed):
    print("  -", c)

print("\n=== P5 : META DESCRIPTIONS > 155 CAR (à raccourcir) ===")
for L, name in sorted(meta_report, reverse=True):
    print(f"  {L}  {name}")
if not meta_report:
    print("  (aucune)")
