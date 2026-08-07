# Spec de rédaction des articles de blog - Les Éclairés

Source de vérité pour la génération d'articles (automatisation N8N incluse).
Thématique du site : bornes de recharge électrique / IRVE, France entière.
Dernière mise à jour : 2026-08-04.

Un article n'est conforme que s'il respecte TOUS les points ci-dessous.
Articles de référence à imiter : `choisir-installateur-irve-certifie.html` et
`prise-renforcee-ou-borne-de-recharge.html`.

---

## 1. Fichier et gabarit

- Un article = un fichier `blog/<slug>.html`.
- Base = `blog/template.html`, avec des placeholders `%%...%%` à remplacer :

| Placeholder | Contenu attendu |
|---|---|
| `%%SEO_TITLE%%` | `<title>`, 60 caractères max, mot-clé en tête |
| `%%META_DESC%%` | meta description, 160 caractères max, mot-clé au début |
| `%%SLUG%%` | slug propre (sert au canonical) |
| `%%DATE_ISO%%` | date `AAAA-MM-JJ` (published_time) |
| `%%CATEGORY%%` | badge : Guide, Comparatif, Prix, Aides, Technique... |
| `%%TITRE%%` | H1 affiché |
| `%%DATE_FR%%` | date lisible, ex. « 4 août 2026 » |
| `%%READ_TIME%%` | ex. « 6 min » |
| `%%TOC_ITEMS%%` | un `<li><a href="#id">...</a></li>` par H2 |
| `%%ARTICLE_HTML%%` | corps de l'article |

Après remplacement, il ne doit rester AUCUN `%%` dans le fichier.

## 2. Bloc SEO a injecter juste avant `</head>` (obligatoire)

`template.html` ne contient PAS de JSON-LD : il faut l'ajouter.

```html
<meta property="og:url" content="https://leseclaires.fr/blog/<slug>.html">
<meta property="og:title" content="<SEO_TITLE>">
<meta property="og:image" content="https://leseclaires.fr/hero.jpg">
<meta property="article:modified_time" content="<AAAA-MM-JJ>T00:00:00+01:00">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting",
"headline":"...","description":"...","image":"https://leseclaires.fr/hero.jpg",
"url":"https://leseclaires.fr/blog/<slug>.html",
"mainEntityOfPage":{"@type":"WebPage","@id":"https://leseclaires.fr/blog/<slug>.html"},
"datePublished":"...","dateModified":"...",
"author":{"@type":"Organization","name":"Les Éclairés","url":"https://leseclaires.fr/"},
"publisher":{"@type":"Organization","name":"Les Éclairés","logo":{"@type":"ImageObject","url":"https://leseclaires.fr/favicon.png"}}}</script>
```

Si l'article a une FAQ, ajouter un SECOND bloc `"@type":"FAQPage"` reprenant les
questions/réponses réellement affichées.

Tout JSON-LD doit être un JSON valide (à parser avant écriture).

## 3. Structure du corps (`%%ARTICLE_HTML%%`)

- Chaque H2 formulé en QUESTION, avec un `id` : `<h2 id="prix">Combien coute... ?</h2>`.
- Sous chaque H2, une réponse autoportante de 2 lignes max EN PREMIER, avant le
  développement (fragment extrait par Google et les IA).
- Classes du gabarit : `.prose`, `<table>`, `<blockquote>`.
- Un CTA milieu d'article : `<div class="ctamid">...<a href="../index.html#simulateur">...</a></div>`.
- Maillage interne obligatoire : lien vers le simulateur, `/partenaires.html`, et 1 a 2
  autres articles pertinents (pilier prix, 7/22 kW, copropriété...).
- `%%TOC_ITEMS%%` liste exactement les `id` des H2.
- Longueur cible : 1000 a 1500 mots.

## 4. REGLES FACTUELLES 2026 (le point critique)

- Credit d'impot particuliers : SUPPRIME (non reconduit apres le 31/12/2025). Ne
  jamais l'annoncer comme actif. Le mentionner comme supprime si pertinent.
- Prime ADVENIR (copropriete), bareme du 01/04/2026 : jusqu'a 1 000 EUR HT borne
  individuelle, 1 660 EUR HT borne partagee, 12 500 EUR HT infrastructure collective,
  prise en charge 50 %. Pavillons individuels NON eligibles. Dossier valide AVANT travaux.
- TVA 5,5 % (au lieu de 20 %) : pose par pro qualifie IRVE, logement de plus de 2 ans.
- Prix indicatifs (TTC, pose comprise) : borne 7,4 kW environ 1 200 a 2 000 EUR ;
  22 kW environ 2 500 a 3 500 EUR ; prise renforcee environ 500 a 1 000 EUR.
- Qualification IRVE obligatoire au-dela de 3,7 kW (Qualifelec, AFNOR, Qualit'EnR),
  mention IRVE sur le devis ET la facture.

## 5. Regles editoriales

- JAMAIS de tiret cadratin ni demi-cadratin (« — » ou « – »). Utiliser virgule,
  parentheses, ou trait d'union simple « - ». Regle absolue.
- Prix toujours en TTC (preciser HT pour ADVENIR).
- Aucune donnee inventee (pas de faux chiffres, avis ou notes).
- Slug propre, jamais tronque. Mots-cles lisibles, ex. `prix-borne-de-recharge-maison-2026`.
  Interdiction des slugs coupes type `...-quel-prix-total-faut-il-vraime`.
- Sortie = HTML brut UNIQUEMENT. Ne JAMAIS entourer le corps de l'article de
  balises Markdown ` ```html ` ou ` ``` ` : le contenu est injecte tel quel dans
  le template, une cloture de code laisse le texte `\`\`\`html` visible sur la page.

## 6. Enregistrement apres generation (a automatiser aussi)

Un article n'est pas fini tant qu'il n'est pas :
1. Committe dans le repo (`blog/<slug>.html`) sur `main` (sinon Vercel ne le deploie jamais).
2. Ajoute au carrousel de l'accueil `index.html` (voir 6.A) : garder les 3 DERNIERS
   articles, inserer le nouveau en tete, retirer le plus ancien.
3. Ajoute au listing `blog/index.html` (voir 6.B).
4. Ajoute a `sitemap.xml` : `<url><loc>https://leseclaires.fr/blog/<slug>.html</loc><lastmod>AAAA-MM-JJ</lastmod><priority>0.7</priority></url>`
   inseré avant `</urlset>`, avec garde anti-doublon (ne rien faire si l'URL existe deja).

ATTENTION : `index.html` ET `blog/index.html` utilisent tous les deux un conteneur
`<div class="blog-grid">`, mais le FORMAT DE CARTE est DIFFERENT. Ne pas confondre.
Cibler le bon fichier.

### 6.A Carte du carrousel accueil (`index.html`)

Ancre : `<div class="blog-grid">` (inserer la carte juste apres l'ouverture = en tete).
Format :

```html
<a href="blog/<slug>.html" class="blog-card reveal rd1">
  <div class="blog-thumb blog-thumb-1">
    <emoji>
    <span class="blog-tag"><category></span>
  </div>
  <div class="blog-body">
    <div class="blog-date"><Mois AAAA></div>
    <div class="blog-title"><titre></div>
    <div class="blog-excerpt"><desc courte></div>
    <span class="blog-cta">Lire l article →</span>
  </div>
</a>
```

Emoji indicatif selon le sujet (prix -> maison, aides -> eclair, technique -> prise,
copro -> immeuble). Ne garder que 3 cartes au total (retirer la plus ancienne).

### 6.B Carte du listing blog (`blog/index.html`)

Ancre (par ordre de priorite, la 1re trouvee) :
`<div class="blog-grid">`, puis `<div class="blog-list">`, `<div class="articles">`,
`<div id="articles">`, `<main`.
Aujourd'hui seul `<div class="blog-grid">` existe : il DOIT etre en tete de la liste
d'ancres. Inserer la carte juste apres l'ouverture du div (le plus recent en tete).
Format :

```html
<a class="blog-card" href="/blog/<slug>.html">
          <span class="bc-tag"><category></span>
          <span class="bc-date"><Mois AAAA></span>
          <h2><titre></h2>
          <p><desc 160 car></p>
          <span class="bc-more">Lire l'article →</span>
        </a>
```

`bc-date` = texte lisible (« Août 2026 »), jamais une date ISO. `bc-tag` = meme valeur
que le badge `%%CATEGORY%%`. Garde anti-doublon : ne pas inserer si `/blog/<slug>.html`
est deja present.

## 7. Anti-cannibalisation (obligatoire avant de generer)

Une intention de recherche = un seul article. Avant de creer, verifier qu'aucun
article existant ne cible deja le meme mot-cle / la meme intention. Si c'est le cas,
METTRE A JOUR l'article existant au lieu d'en creer un doublon.

Historique : 4 articles quasi identiques sur « prix borne maison » avaient ete
generes et se cannibalisaient. Ils ont ete consolides en un pilier unique
(`prix-borne-de-recharge-maison-2026.html`) avec redirections 301.
