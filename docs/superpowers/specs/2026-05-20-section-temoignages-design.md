# Section "Témoignages" — Design

**Date** : 2026-05-20
**Statut** : Validé par Enza, prêt pour implémentation
**Type** : Nouvelle section sur `index.html`

## Contexte

Le site Enza ne contient aucun témoignage de patient à ce jour. L'objectif est d'augmenter la confiance des visiteurs en ajoutant une section dédiée, sans recourir à un système de notation (étoiles, scores) qui n'est pas adapté à une pratique de musicothérapie.

Un premier témoignage a été recueilli auprès de Virginie (intervention en institut auprès de sa mère atteinte d'Alzheimer). La section doit pouvoir l'accueillir seul au lancement, et grandir naturellement à mesure que d'autres témoignages sont collectés.

Les témoignages sont publiés par Enza elle-même, jamais soumis librement par les visiteurs — ce choix est documenté dans une note de design séparée et découle de contraintes RGPD et déontologiques propres aux professions de santé.

## Décisions de design

### Emplacement

- Sur `index.html`, entre la section `#seances` et la section `#ressources`.
- Une seule section HTML avec `id="temoignages"`.
- Ordre des sections : Hero → À propos → Approche → Séances → **Témoignages** → Ressources → FAQ → Contact.

Raison : le visiteur a d'abord besoin de comprendre l'approche et l'offre. Les témoignages arrivent au moment où il se demande "ça marche, sur qui ?" — preuve sociale après le quoi, avant les contenus et la conversion.

### Structure visuelle

- Bloc centré, largeur max **720px**, padding section identique aux autres sections crème.
- Fond `var(--cream)`.
- En-tête centré :
  - Tag `TÉMOIGNAGES` — capsule à bordure verte (style identique au `.section-tag` des articles et du blog, pas à celui de l'index actuel — voir Cohérence ci-dessous).
  - Titre *Ce qu'en disent les personnes accompagnées* — `Cormorant Garamond` italique, taille `2rem`, couleur `--slate`.
  - **Note de consentement** sous le titre, en italique gris clair (`--slate-mid`, taille `~0.85rem`) : *Témoignages partagés avec l'accord des personnes concernées. Prénoms modifiés à la demande.*
- Liste verticale des témoignages, chacun séparé par un trait fin `1px solid rgba(122,158,126,0.25)`.

### Format d'un témoignage

- Citation en `Cormorant Garamond` italique, taille `1.15rem`, line-height `1.7`, couleur `--slate`.
- Guillemets français `«` et `»` placés **uniquement** au début du premier paragraphe et à la fin du dernier paragraphe du témoignage — jamais autour de chaque paragraphe individuel, pour ne pas donner l'illusion de plusieurs témoignages distincts.
- Plusieurs paragraphes possibles dans un même témoignage (séparés par un `<p>` mais sans guillemet).
- Attribution sous le témoignage en `DM Sans`, taille `0.72rem`, `letter-spacing: 0.18em`, `text-transform: uppercase`, couleur `--slate-mid`.
- Format d'attribution : `Prénom · Contexte`. Pas d'âge, pas de nom de famille.

### Contenu au lancement

Un seul témoignage publié :

> « J'ai accompagné ma maman, atteinte de la maladie d'Alzheimer sévère, pour une séance de musicothérapie avec Enza, et l'expérience a été très positive. Enza fait preuve d'une grande bienveillance, de douceur et d'une écoute attentive, ce qui met rapidement en confiance. Elle a su créer un cadre apaisant et adapté, dans lequel ma maman s'est sentie à l'aise et réceptive.
>
> La séance s'est déroulée dans une atmosphère sereine et respectueuse du rythme de chacun. On sent une réelle envie d'aider et d'accompagner avec le cœur, ce qui est précieux dans ce type d'accompagnement.
>
> Même si elle est encore en début de parcours, son approche est déjà très prometteuse. Je recommande Enza pour sa gentillesse, son implication et la qualité de sa présence. »

**Attribution** : *Virginie · Intervention en Institut*

### Mécanisme d'expansion

- Tant que la section contient **3 témoignages ou moins**, tous sont affichés directement, pas de bouton.
- À partir de **4 témoignages**, les 2 ou 3 premiers sont visibles par défaut et les suivants sont masqués (`hidden`).
- Bouton sous la liste, libellé *Lire d'autres témoignages (N)* où N est le nombre de témoignages masqués.
- Au clic, les témoignages masqués apparaissent avec une transition douce (`max-height` ou simple `display`), le bouton disparaît ou se transforme en *Replier*.
- Accessibilité : `aria-expanded`, `aria-controls` corrects.

Pour le lancement avec un seul témoignage, le bouton n'est pas affiché. Le HTML et le JS doivent néanmoins être structurés pour permettre l'ajout futur sans refonte.

### Animations

- La section utilise la classe `.fade-up` comme les autres sections du site pour cohérence (animation à l'apparition au scroll).

### Pas inclus

- Aucun CTA à la fin de la section. Le flow naturel de la page (Ressources → FAQ → Contact) gère la conversion.
- Aucun visuel, photo ou icône.
- Pas de système d'avis libre soumis par les visiteurs (décidé hors de cette spec).
- Pas de carrousel, pas d'onglets, pas de scroll interne indépendant.
- Pas de notation par étoiles.

## Cohérence avec le reste du site

### Variable de couleur

Utiliser les variables CSS existantes : `--cream`, `--slate`, `--slate-mid`, `--green`, `--green-light`. Aucune nouvelle variable.

### Composant `section-tag`

Le site a deux styles divergents pour `section-tag` (issue détectée dans l'audit) :
- `index.html` : sans bordure, taille `0.58rem`
- `blog.html` et articles : avec bordure verte, taille `0.62rem`

Pour cette nouvelle section sur `index.html`, utiliser **le style des articles/blog** (avec bordure). Cela introduit une légère incohérence locale dans `index.html` qui pourra être résolue dans un chantier ultérieur d'harmonisation des composants (non couvert par cette spec).

### Typographie

Réutiliser exactement les familles déjà chargées : `DM Sans` et `Cormorant Garamond`. Aucun import nouveau.

## Implications hors section

### Mentions légales

Mise à jour de `mentions-legales.html` pour ajouter, dans la section RGPD, une mention sur le traitement des témoignages :
- Consentement explicite recueilli avant publication.
- Anonymisation (prénom seul, contexte général, pas d'âge ni de nom).
- Droit de retrait à tout moment sur simple demande par email.
- Durée de conservation : tant que pertinent pour la communication du site, retrait sur demande sans délai.

L'ajout se fait dans la section `#donnees` existante, sous une nouvelle sous-section `<h3>Témoignages</h3>`.

### Modification de l'ordre des sections sur l'index

L'ajout entre `#seances` et `#ressources` ne casse aucun lien interne existant. Les ancres `#approche`, `#seances`, `#contact` restent valides. Ajouter `#temoignages` comme ancre, ne pas l'inclure dans le menu de navigation principal (sobriété).

## Critères de validation

L'implémentation est complète quand :

1. La nouvelle section est visible sur `index.html` entre Séances et Ressources.
2. Le témoignage de Virginie s'affiche avec la mise en forme spécifiée (citation italique, guillemets uniquement aux extrémités, attribution en uppercase).
3. La note de consentement est visible et discrète sous le titre.
4. La section est responsive (lisible sur mobile, max-width respecté sur desktop).
5. L'animation `fade-up` se déclenche au scroll.
6. La structure HTML/JS permet d'ajouter d'autres témoignages en modifiant uniquement le contenu (pas le CSS ni le JS).
7. Le bouton *Lire d'autres témoignages* apparaît automatiquement quand 4+ témoignages sont présents.
8. Les mentions légales contiennent la sous-section sur les témoignages.
9. Aucune régression visuelle sur les sections adjacentes (Séances, Ressources).
10. Validation manuelle sur Chrome desktop et mobile (DevTools responsive).
