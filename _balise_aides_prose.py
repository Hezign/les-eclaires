#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brique 3 (extension 3a) : balisage data-aide de la PROSE visible + TVA + prix.
Ne touche JAMAIS le JSON-LD (valeurs en <script> laissées telles quelles).
Ancres à contexte unique. fmt : 'pct' (taux*100), 'range_eur' (min à max €).
Idempotent (skip si déjà balisé).
"""
import pathlib
BLOG = pathlib.Path(__file__).parent / "blog"

def sp(path, text, fmt=None):
    a = f' data-aide-fmt="{fmt}"' if fmt else ''
    return f'<span data-aide="{path}"{a}>{text}</span>'

EDITS = [
 # ---------- guide-prime (€) : paragraphe intro (238) ----------
 ("guide-prime-advenir-2026.html",
  "<strong>1 000 € HT par point de charge</strong> pour une borne individuelle",
  f"<strong>{sp('advenir.copropriete.borne_individuelle.montant_ht','1 000 € HT')} par point de charge</strong> pour une borne individuelle"),
 ("guide-prime-advenir-2026.html",
  "1 660 € HT pour une borne partagée (barèmes",
  f"{sp('advenir.copropriete.borne_partagee.montant_ht','1 660 € HT')} pour une borne partagée (barèmes"),
 # ---------- guide-prime (€) : paragraphe barème (243) ----------
 ("guide-prime-advenir-2026.html",
  "jusqu'à 1 000 € HT pour une borne individuelle",
  f"jusqu'à {sp('advenir.copropriete.borne_individuelle.montant_ht','1 000 € HT')} pour une borne individuelle"),
 ("guide-prime-advenir-2026.html",
  "1 660 € HT pour une borne partagée et 12 500 € HT pour une infrastructure collective jusqu'à 100 places (<strong>+ 125 € HT par place au-delà</strong>)",
  f"{sp('advenir.copropriete.borne_partagee.montant_ht','1 660 € HT')} pour une borne partagée et {sp('advenir.copropriete.infrastructure_collective.montant_ht','12 500 € HT')} pour une infrastructure collective jusqu'à 100 places (<strong>+ {sp('advenir.copropriete.infrastructure_collective.majoration_par_place_au_dela_ht','125 € HT')} par place au-delà</strong>)"),
 ("guide-prime-advenir-2026.html",
  "jusqu'à <strong>8 000 € HT</strong> de travaux de voirie et réseaux (VRD, + 80 € HT par place extérieure au-delà de 100)",
  f"jusqu'à <strong>{sp('advenir.copropriete.surprime_vrd.montant_ht','8 000 € HT')}</strong> de travaux de voirie et réseaux (VRD, + {sp('advenir.copropriete.surprime_vrd.majoration_par_place_ext_au_dela_de_100_ht','80 € HT')} par place extérieure au-delà de 100)"),
 ("guide-prime-advenir-2026.html",
  "jusqu'à <strong>3 000 € HT</strong> pour la création d'un point de livraison",
  f"jusqu'à <strong>{sp('advenir.copropriete.surprime_point_livraison.montant_ht','3 000 € HT')}</strong> pour la création d'un point de livraison"),

 # ---------- financement (EUR) : intro (239) ----------
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "avec un plafond atteignant 12 500 EUR HT.",
  f"avec un plafond atteignant {sp('advenir.copropriete.infrastructure_collective.montant_ht','12 500 EUR HT')}."),
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "notamment la TVA réduite à 5,5 % sur la pose",
  f"notamment la TVA réduite à {sp('tva.borne_recharge.taux','5,5 %','pct')} sur la pose"),
 # ---------- financement (EUR) : énoncé principal (258) ----------
 ("financement-infrastructure-collective-copropriete-advenir-2026.html",
  "avec un plafond de 12 500 EUR HT pour une infrastructure collective complète jusqu'à 100 places, majoré de 125 EUR HT par place au-delà.",
  f"avec un plafond de {sp('advenir.copropriete.infrastructure_collective.montant_ht','12 500 EUR HT')} pour une infrastructure collective complète jusqu'à 100 places, majoré de {sp('advenir.copropriete.infrastructure_collective.majoration_par_place_au_dela_ht','125 EUR HT')} par place au-delà."),

 # ---------- prise-renforcee : TVA prose visible (249) ----------
 ("prise-renforcee-ou-borne-de-recharge.html",
  "bénéficie de la TVA réduite à 5,5 % (article 278-0 bis N du CGI)",
  f"bénéficie de la TVA réduite à {sp('tva.borne_recharge.taux','5,5 %','pct')} (article 278-0 bis N du CGI)"),
 ("prise-renforcee-ou-borne-de-recharge.html",
  "relève elle du taux intermédiaire de 10 % applicable",
  f"relève elle du taux intermédiaire de {sp('tva.prise_renforcee.taux','10 %','pct')} applicable"),
 # ---------- prise-renforcee : tableau prix (245-247) ----------
 ("prise-renforcee-ou-borne-de-recharge.html",
  "<td>500 à 1 000 €</td><td>~3,2 kW</td>",
  f"<td>{sp('prix_indicatifs_ttc.prise_renforcee','500 à 1 000 €','range_eur')}</td><td>~3,2 kW</td>"),
 ("prise-renforcee-ou-borne-de-recharge.html",
  "<td>1 200 à 2 000 €</td><td>7,4 kW</td>",
  f"<td>{sp('prix_indicatifs_ttc.borne_7_4_kw','1 200 à 2 000 €','range_eur')}</td><td>7,4 kW</td>"),
 ("prise-renforcee-ou-borne-de-recharge.html",
  "<td>2 500 à 3 500 €</td><td>22 kW</td>",
  f"<td>{sp('prix_indicatifs_ttc.borne_22_kw','2 500 à 3 500 €','range_eur')}</td><td>22 kW</td>"),
]

applied, skipped, errors = 0, 0, []
for fname, old, new in EDITS:
    f = BLOG / fname
    t = f.read_text(encoding="utf-8")
    if new in t:
        skipped += 1; continue
    n = t.count(old)
    if n == 0:   errors.append(f"{fname}: introuvable -> {old[:55]!r}"); continue
    if n > 1:    errors.append(f"{fname}: ambigu ({n}x) -> {old[:55]!r}"); continue
    f.write_text(t.replace(old, new, 1), encoding="utf-8"); applied += 1

print(f"Balises prose/TVA/prix : appliquées {applied} | déjà là {skipped} | erreurs {len(errors)}")
for e in errors: print("  !!", e)
for fname in dict.fromkeys(e[0] for e in EDITS):
    print(f"  {(BLOG/fname).read_text(encoding='utf-8').count('data-aide='):2d} balises data-aide au total dans {fname}")
