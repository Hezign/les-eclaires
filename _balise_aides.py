#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brique 3 (v1) : balisage data-aide des valeurs ADVENIR dans les tableaux de barème
des 3 pages de référence. Chaque montant affiché est enveloppé d'un
<span data-aide="chemin.dans.aides.json">…</span> (texte visible inchangé),
pour permettre la propagation automatique depuis data/aides.json.
Idempotent (ne re-balise pas si data-aide déjà présent sur la cellule).
"""
import pathlib
BLOG = pathlib.Path(__file__).parent / "blog"

def span(path, text):
    return f'<span data-aide="{path}">{text}</span>'

# (fichier, cellule_old, cellule_new)
EDITS = [
 # ---- guide-prime (€) ----
 ("guide-prime-advenir-2026.html",
  "<td>Jusqu'à 1 000 € HT / point</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.borne_individuelle.montant_ht','1 000 € HT')} / point</td>"),
 ("guide-prime-advenir-2026.html",
  "<td>Jusqu'à 1 660 € HT / point</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.borne_partagee.montant_ht','1 660 € HT')} / point</td>"),
 ("guide-prime-advenir-2026.html",
  "<td>Jusqu'à 12 500 € HT (jusqu'à 100 places, + 125 € HT / place au-delà)</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.infrastructure_collective.montant_ht','12 500 € HT')} (jusqu'à 100 places, + {span('advenir.copropriete.infrastructure_collective.majoration_par_place_au_dela_ht','125 € HT')} / place au-delà)</td>"),
 ("guide-prime-advenir-2026.html",
  "<td>Jusqu'à 8 000 € HT (+ 80 € HT / place ext. au-delà de 100)</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.surprime_vrd.montant_ht','8 000 € HT')} (+ {span('advenir.copropriete.surprime_vrd.majoration_par_place_ext_au_dela_de_100_ht','80 € HT')} / place ext. au-delà de 100)</td>"),
 ("guide-prime-advenir-2026.html",
  "<td>Jusqu'à 3 000 € HT</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.surprime_point_livraison.montant_ht','3 000 € HT')}</td>"),

 # ---- financement (EUR) ----
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "<td>1 000 EUR HT</td>",
  f"<td>{span('advenir.copropriete.borne_individuelle.montant_ht','1 000 EUR HT')}</td>"),
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "<td>1 660 EUR HT</td>",
  f"<td>{span('advenir.copropriete.borne_partagee.montant_ht','1 660 EUR HT')}</td>"),
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "<td>12 500 EUR HT (jusqu'à 100 places, + 125 EUR HT / place au-delà)</td>",
  f"<td>{span('advenir.copropriete.infrastructure_collective.montant_ht','12 500 EUR HT')} (jusqu'à 100 places, + {span('advenir.copropriete.infrastructure_collective.majoration_par_place_au_dela_ht','125 EUR HT')} / place au-delà)</td>"),
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "<td>8 000 EUR HT (+ 80 EUR HT / place ext. au-delà de 100)</td>",
  f"<td>{span('advenir.copropriete.surprime_vrd.montant_ht','8 000 EUR HT')} (+ {span('advenir.copropriete.surprime_vrd.majoration_par_place_ext_au_dela_de_100_ht','80 EUR HT')} / place ext. au-delà de 100)</td>"),
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "<td>3 000 EUR HT</td>",
  f"<td>{span('advenir.copropriete.surprime_point_livraison.montant_ht','3 000 EUR HT')}</td>"),

 # ---- devenir-installateur (EUR, / point) ----
 ("devenir-installateur-agree-advenir.html",
  "<td>Jusqu'à 1 000 EUR HT / point</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.borne_individuelle.montant_ht','1 000 EUR HT')} / point</td>"),
 ("devenir-installateur-agree-advenir.html",
  "<td>Jusqu'à 1 660 EUR HT / point</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.borne_partagee.montant_ht','1 660 EUR HT')} / point</td>"),
 ("devenir-installateur-agree-advenir.html",
  "<td>Jusqu'à 12 500 EUR HT (jusqu'à 100 places, + 125 EUR HT / place au-delà)</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.infrastructure_collective.montant_ht','12 500 EUR HT')} (jusqu'à 100 places, + {span('advenir.copropriete.infrastructure_collective.majoration_par_place_au_dela_ht','125 EUR HT')} / place au-delà)</td>"),
 ("devenir-installateur-agree-advenir.html",
  "<td>Jusqu'à 8 000 EUR HT</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.surprime_vrd.montant_ht','8 000 EUR HT')}</td>"),
 ("devenir-installateur-agree-advenir.html",
  "<td>Jusqu'à 3 000 EUR HT</td>",
  f"<td>Jusqu'à {span('advenir.copropriete.surprime_point_livraison.montant_ht','3 000 EUR HT')}</td>"),
]

applied, skipped, errors = 0, 0, []
for fname, old, new in EDITS:
    f = BLOG / fname
    t = f.read_text(encoding="utf-8")
    if new in t:
        skipped += 1; continue
    n = t.count(old)
    if n == 0:
        errors.append(f"{fname}: cellule introuvable -> {old[:45]!r}"); continue
    if n > 1:
        errors.append(f"{fname}: cellule ambiguë ({n}x) -> {old[:45]!r}"); continue
    f.write_text(t.replace(old, new, 1), encoding="utf-8"); applied += 1

print(f"Balises appliquées: {applied} | déjà présentes: {skipped} | erreurs: {len(errors)}")
for e in errors: print("  !!", e)

# récapitulatif : combien de data-aide par fichier
for fname in dict.fromkeys(e[0] for e in EDITS):
    c = (BLOG/fname).read_text(encoding="utf-8").count("data-aide=")
    print(f"  {c:2d} balises data-aide dans {fname}")
