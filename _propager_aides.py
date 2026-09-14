#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brique 3 (propagation) : lit data/aides.json (source de vérité) et réécrit le
contenu de chaque <span data-aide="chemin" [data-aide-fmt="..."]>…</span> du site.

Principe : on ne reconstruit pas le texte, on remplace seulement le(s) jeton(s)
numérique(s) DANS le texte existant. Ainsi la devise (€ / EUR), les suffixes
(HT), la langue et la ponctuation sont préservés. Séparateur de milliers =
espace normal (convention du site).

fmt :
  (défaut)     valeur = nombre  -> remplace le 1er entier du span
  pct          valeur = taux (0.055) -> remplace le nombre (virgule décimale) par taux*100
  range_eur    valeur = {min,max} -> remplace les 2 premiers entiers par min puis max

Lancer : python3 _propager_aides.py          (applique)
         python3 _propager_aides.py --check   (échoue si des écarts existent, pour la CI)
Idempotent.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
AIDES = json.loads((ROOT / "data" / "aides.json").read_text(encoding="utf-8"))

SEP = " "  # séparateur de milliers utilisé sur le site (espace normal)
# entier avec séparateurs de milliers éventuels (espace normal, insécable, fine)
NUM = "\\d[\\d   ]*\\d|\\d"
# décimal pour les taux : « 5,5 » ou « 10 »
PCT_NUM = r"\d+(?:,\d+)?"
SPAN = re.compile(r'(<span data-aide="([^"]+)"(?: data-aide-fmt="([^"]+)")?>)(.*?)(</span>)')

def resolve(path):
    cur = AIDES
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur

def fr_int(n):
    return f"{int(round(float(n))):,}".replace(",", SEP)

def fr_num(x):
    x = float(x)
    return str(int(x)) if x == int(x) else ("%g" % x).replace(".", ",")

def new_inner(path, fmt, inner):
    val = resolve(path)
    if val is None:
        return inner, f"clé absente: {path}"
    if fmt == "pct":
        return re.sub(PCT_NUM, fr_num(float(val) * 100), inner, count=1), None
    if fmt == "range_eur":
        if not isinstance(val, dict) or "min" not in val or "max" not in val:
            return inner, f"valeur non-range: {path}"
        parts = re.split(f"({NUM})", inner)
        seen = 0; repl = [fr_int(val["min"]), fr_int(val["max"])]
        for i, p in enumerate(parts):
            if p and re.fullmatch(NUM, p) and seen < 2:
                parts[i] = repl[seen]; seen += 1
        return "".join(parts), None
    if isinstance(val, dict):
        return inner, f"attendu scalaire, reçu objet: {path}"
    return re.sub(NUM, lambda m: fr_int(val), inner, count=1), None

def process(text):
    changes = []; warns = []
    def sub(m):
        open_, path, fmt, inner, close = m.groups()
        ni, warn = new_inner(path, fmt, inner)
        if warn: warns.append(warn)
        if ni != inner:
            changes.append((path, inner.strip(), ni.strip()))
        return open_ + ni + close
    return SPAN.sub(sub, text), changes, warns

def main():
    check = "--check" in sys.argv
    files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "blog").glob("*.html"))
    total = 0; all_warns = []
    for f in files:
        t = f.read_text(encoding="utf-8")
        if "data-aide=" not in t:
            continue
        nt, changes, warns = process(t)
        all_warns += [(f.name, w) for w in warns]
        if changes:
            total += len(changes)
            print(f"\n{f.relative_to(ROOT)} : {len(changes)} valeur(s)")
            for path, old, new in changes:
                print(f"    {path}: {old!r} -> {new!r}")
            if not check:
                f.write_text(nt, encoding="utf-8")
    if all_warns:
        print("\nAVERTISSEMENTS :")
        for name, w in all_warns:
            print(f"  {name}: {w}")
    if total == 0:
        print("Site déjà cohérent avec data/aides.json (0 changement).")
    if check and total:
        print(f"\n[--check] {total} écart(s) : le site n'est pas à jour avec aides.json.")
        sys.exit(1)

if __name__ == "__main__":
    main()
