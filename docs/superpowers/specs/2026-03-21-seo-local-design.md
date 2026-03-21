# SEO Local — Enza Duhem Musicothérapeute
**Date:** 2026-03-21
**Objectif:** Faire apparaître le site dans les premiers résultats Google pour les recherches locales de musicothérapie (Tournai, Hainaut, Belgique)

---

## Contexte

Site statique hébergé sur Netlify : `musicotherapeute-hainaut.be`
Pages existantes : `index.html`, `blog.html`, `mentions-legales.html`, `confirmation.html`
SEO actuel : titres basiques, meta descriptions partielles, pas de schema, pas de sitemap, pas de robots.txt

**Objectif de classement :** Recherches locales uniquement — "musicothérapie Tournai", "musicothérapeute Hainaut", "musicothérapeute à domicile Belgique"

---

## Section 1 — SEO Technique du site

### 1.1 Titres optimisés (title tags)
- `index.html` → `Musicothérapeute à Tournai & Hainaut | Enza Duhem`
- `blog.html` → `Ressources en musicothérapie — Hainaut`
- `mentions-legales.html` → `Mentions légales | Enza Duhem`
- `confirmation.html` → `Message envoyé | Enza Duhem` (noindex)

### 1.2 Meta descriptions améliorées
- `index.html` : inclure "musicothérapeute", "Tournai", "Hainaut", "séances à domicile"
- `blog.html` : inclure "musicothérapie", "articles", "ressources", "Hainaut"

### 1.3 JSON-LD Schema (données structurées)
Ajouter dans `<head>` de `index.html` un bloc `<script type="application/ld+json">` avec :
- Type : `LocalBusiness` + `Person`
- Nom : Enza Duhem
- Profession : Musicothérapeute
- Adresse : Vaulx, Tournai, Hainaut, Belgique
- URL : https://musicotherapeute-hainaut.be
- Email : enza@musicotherapeute-hainaut.be
- Zone de service : Hainaut, Tournai, Belgique
- Langue : fr-BE

### 1.4 Open Graph tags
Ajouter dans `<head>` de `index.html` et `blog.html` :
- `og:title`, `og:description`, `og:url`, `og:image` (hero-bg.jpg)
- `og:type` : website
- `og:locale` : fr_BE

### 1.5 robots.txt
Créer `robots.txt` à la racine :
```
User-agent: *
Allow: /
Disallow: /confirmation.html
Sitemap: https://musicotherapeute-hainaut.be/sitemap.xml
```

### 1.6 sitemap.xml
Créer `sitemap.xml` à la racine avec les 3 pages publiques :
- `https://musicotherapeute-hainaut.be/` (priority: 1.0)
- `https://musicotherapeute-hainaut.be/blog.html` (priority: 0.8)
- `https://musicotherapeute-hainaut.be/mentions-legales.html` (priority: 0.3)

### 1.7 Meta robots sur confirmation.html
Ajouter `<meta name="robots" content="noindex, nofollow">` sur `confirmation.html` (page de remerciement, inutile à indexer)

### 1.8 Canonical URLs
Ajouter `<link rel="canonical" href="https://musicotherapeute-hainaut.be/">` sur chaque page.

---

## Section 2 — Google Business Profile

Action manuelle effectuée par Enza sur [business.google.com](https://business.google.com).

### Données à renseigner
- **Nom :** Enza Duhem — Musicothérapeute
- **Catégorie :** Musicothérapeute (catégorie principale)
- **Type :** Prestataire de services à domicile (zone de service, pas d'adresse publique)
- **Zone de service :** Tournai, Hainaut
- **Site web :** https://musicotherapeute-hainaut.be
- **Email :** enza@musicotherapeute-hainaut.be
- **Description :** texte optimisé avec mots-clés locaux (à rédiger)
- **Photos :** hero-bg.jpg, ressources-bg.jpg

### Vérification
Google envoie un code de vérification (SMS ou courrier) — obligatoire pour apparaître sur Maps.

---

## Section 3 — Google Search Console

Action manuelle effectuée par Enza sur [search.google.com/search-console](https://search.google.com/search-console).

### Étapes
1. Ajouter la propriété `https://musicotherapeute-hainaut.be`
2. Vérifier via balise HTML meta → on ajoute la balise dans `<head>` de `index.html`
3. Soumettre `https://musicotherapeute-hainaut.be/sitemap.xml`

### Bénéfices
- Indexation en 24-48h
- Suivi des mots-clés et clics
- Alertes en cas de problème technique

---

## Fichiers à modifier / créer

| Fichier | Action |
|---|---|
| `index.html` | Modifier title, meta description, ajouter JSON-LD, Open Graph, canonical |
| `blog.html` | Modifier title, meta description, ajouter Open Graph, canonical |
| `mentions-legales.html` | Modifier title, ajouter canonical |
| `confirmation.html` | Ajouter noindex, canonical |
| `robots.txt` | Créer (nouveau) |
| `sitemap.xml` | Créer (nouveau) |

---

## Hors périmètre
- SEO national / mot-clé "musicothérapie" général (trop compétitif)
- Netlify CMS / blog dynamique
- Backlinks / netlinking (long terme)
- Google Ads (payant)
