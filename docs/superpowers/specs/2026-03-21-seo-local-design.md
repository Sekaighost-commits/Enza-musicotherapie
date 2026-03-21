# SEO Local — Enza Duhem Musicothérapeute
**Date:** 2026-03-21
**Objectif:** Faire apparaître le site dans les premiers résultats Google pour les recherches locales de musicothérapie (Tournai, Hainaut, Belgique)

---

## Contexte

Site statique hébergé sur Netlify : `musicotherapeute-hainaut.be`
Pages existantes : `index.html`, `blog.html`, `mentions-legales.html`, `confirmation.html`
SEO actuel : titres basiques, meta descriptions partielles, pas de schema, pas de sitemap
Note : `robots.txt` et `sitemap.xml` existent déjà à la racine et correspondent au spec — pas à recréer.
Note : `confirmation.html` a déjà `noindex, nofollow` — pas à modifier.

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
Ajouter dans `<head>` de `index.html` un bloc `<script type="application/ld+json">` structuré en `@graph` avec deux nœuds :
- `HealthAndBeautyBusiness` (type principal, plus précis que `LocalBusiness` pour une professionnelle de santé)
  - Nom : Enza Duhem — Musicothérapeute
  - Adresse : Vaulx, Tournai, Hainaut, Belgique (PostalAddress)
  - URL : https://musicotherapeute-hainaut.be
  - Email : enza@musicotherapeute-hainaut.be ⚠️ PLACEHOLDER — à confirmer avant mise en ligne
  - `areaServed` : tableau d'`AdministrativeArea` → Tournai, Hainaut, Belgique
  - `inLanguage` : fr-BE
- `Person`
  - Nom : Enza Duhem
  - Profession (jobTitle) : Musicothérapeute
  - `worksFor` → référence au nœud `HealthAndBeautyBusiness`

⚠️ Structure `@graph` obligatoire pour combiner deux types — ne pas les fusionner dans un seul objet.

### 1.4 Open Graph tags
Ajouter dans `<head>` de `index.html` et `blog.html` :
- `og:title`, `og:description`, `og:url`, `og:image` (hero-bg.jpg)
- `og:image:width` : 1200, `og:image:height` : 630 (format recommandé Facebook/LinkedIn)
- `og:type` : website
- `og:locale` : fr_BE

Note : les balises `html lang` seront également mises à jour de `fr` vers `fr-BE` sur toutes les pages pour cohérence avec og:locale.

### 1.5 robots.txt
✅ Déjà présent et conforme à la racine — aucune action requise.

### 1.6 sitemap.xml
✅ Déjà présent et conforme à la racine — aucune action requise.

### 1.7 confirmation.html
✅ `noindex, nofollow` déjà présent — aucune modification de robots nécessaire.
**Action unique :** ajouter `<link rel="canonical" href="https://musicotherapeute-hainaut.be/confirmation.html">` uniquement.

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

### 1.9 Redirects dans netlify.toml
Vérifier et activer la règle de redirection `www → apex` pour `musicotherapeute-hainaut.be` afin que les canonicals soient cohérents. La règle existe en commentaire dans `netlify.toml` mais référence l'ancien domaine — à mettre à jour.

---

## Fichiers à modifier / créer

| Fichier | Action |
|---|---|
| `index.html` | Modifier title, meta description, ajouter JSON-LD, Open Graph, canonical |
| `blog.html` | Modifier title, meta description, ajouter Open Graph, canonical |
| `mentions-legales.html` | Modifier title, ajouter canonical (tag `noindex, follow` existant conservé — page légale, non destinée à être indexée) |
| `confirmation.html` | Ajouter canonical uniquement (noindex déjà présent) |
| `robots.txt` | Déjà présent et conforme — aucune modification |
| `sitemap.xml` | Déjà présent et conforme — aucune modification |
| `netlify.toml` | Mettre à jour la règle de redirection www → apex |

---

## Hors périmètre
- SEO national / mot-clé "musicothérapie" général (trop compétitif)
- Netlify CMS / blog dynamique
- Backlinks / netlinking (long terme)
- Google Ads (payant)
