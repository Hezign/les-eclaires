#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finitions typographiques françaises, sur le TEXTE visible uniquement
(jamais dans <script>, <style>, <head> ni dans les attributs). Idempotent.

- espace insécable avant ? ! : ; et à l'intérieur des guillemets « »
  (évite le « ? » seul en début de ligne) ;
- espace insécable dans les nombres (1 660, 12 500) et avant € / % / kW / kWh ;
- « EUR » -> « € » (articles n8n) ;
- nombre de questions du simulateur annoncé de façon variable (6, 8, 9, 11) ->
  « quelques questions » dans les CTA du blog.

    python3 _typo.py                 # pages hors accueil + blog
    python3 _typo.py page.html ...
"""
import glob
import os
import re
import sys

NB = ' '

CTA_QUESTIONS = [
    ('<p>8 questions. Une', '<p>Quelques questions. Une'),
    ('Répondez à 6 questions', 'Répondez à quelques questions'),
    ('Répondez à 8 questions', 'Répondez à quelques questions'),
    ('en 8 questions', 'en quelques questions'),
    ('<p>8 questions sur', '<p>Quelques questions sur'),
]


def fix_text(t):
    if not t.strip():
        return t
    t = re.sub(r'(\d)\s?EUR\b', r'\1' + NB + '€', t)
    t = re.sub(r'(?<=\d)[  ](?=\d{3}\b)', NB, t)                  # 1 660 / 12 500
    t = re.sub(r'(?<=\d) (?=(€|%|kWh?\b|kVA\b|km\b|ans?\b|mois\b|jours?\b|h\b|min\b))', NB, t)
    t = re.sub(r'(?<=[^\s\d(\[/]) (?=[?!;:](\s|$|<|&))', NB, t)        # mot ? / mot :
    t = re.sub(r'(?<=[^\s\d(\[/]) (?=[?!;:]$)', NB, t)
    t = re.sub(r'« (?=\S)', '«' + NB, t)
    t = re.sub(r'(?<=\S) »', NB + '»', t)
    return t


def fix_html(s):
    head_end = s.find('</head>')
    head, body = (s[:head_end], s[head_end:]) if head_end != -1 else ('', s)
    for a, b in CTA_QUESTIONS:
        body = body.replace(a, b)
    # découpe : blocs script/style intouchables, balises intouchables, texte corrigé
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', body, flags=re.S)
    out = []
    for p in parts:
        if not p or p.startswith('<'):
            out.append(p)
        else:
            out.append(fix_text(p))
    return head + ''.join(out)


def apply(path):
    try:
        s = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        return False
    n = fix_html(s)
    if n != s:
        open(path, 'w', encoding='utf-8').write(n)
        return True
    return False


def targets():
    fs = [f for f in glob.glob('*.html') if f != 'index.html' and not f.endswith('-preview.html')
          and not os.path.basename(f).startswith(('email-', 'signature-mail'))]
    return fs + glob.glob('villes/*.html') + glob.glob('blog/*.html')


if __name__ == '__main__':
    files = sys.argv[1:] or targets()
    n = sum(apply(f) for f in files)
    print(f'{n} page(s) corrigée(s)')
