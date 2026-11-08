# Charte visuelle

## Le style : une famille, huit visages

**Règle n° 1 : les posts ne doivent pas se ressembler.** L'utilisateur l'exige depuis le 8 novembre 2026. Les premiers posts, tous faits sur le même gabarit, se ressemblaient trop.

- **Ce qui reste constant** (la famille) : les polices (Oswald pour les titres, DM Sans pour le texte, Fraunces italique pour les citations et les idées reçues), les couleurs (vert tendre, crème, vert forêt, vert feuille, sauge, et un **doré** repris des bols chantants de la salle d'Enza), l'adresse du site en bas, le ton calme.
- **Ce qui change d'un post à l'autre** (le visage) : la mise en page, la couleur dominante, la présence d'une photo.
- **Jamais deux posts de suite avec le même visage.** Sur la grille du profil, alterner un post clair, un post foncé et un post avec photo. Le visage de chaque post est noté dans le journal (colonne « format », par exemple `carrousel 5 (idée reçue)`).
- **À l'intérieur d'un carrousel aussi**, on varie : changer de visage ou de `variante` d'une diapo à l'autre (par exemple idée reçue, puis diapo tendre, mots empilés, photo, dernière diapo).
- Polices, couleurs et visages vivent dans `gabarits/theme.css`. Le style B4 (aquarelle, titre crème) choisi au test de style reste l'un des visages. Références : `references-style\` et `posts\propositions-variete\` dans le dossier de travail.

| Visage | Gabarit | Champs | Thèmes conseillés | Fond IA ? |
|---|---|---|---|---|
| 1. Photo de la salle + bandeau | `photo.html` | `photo`, `cadrage`, `label`, `titre` | Coulisses, Pour qui | non |
| 2. Idée reçue / En réalité | `idee-recue.html` | `idee`, `titre`, `texte` | Comprendre | non |
| 3. Chiffre géant | `chiffre.html` | `chiffre` (1 à 3 caractères), `titre`, `texte` | Comprendre, Recherche | non |
| 4. Phrase forte | `citation.html` | `citation`, `label` | Pour qui, Recherche | non |
| 5. Exercice en étapes | `etapes.html` | `label`, `titre`, `etape1` à `etape5` | Une pause pour soi | **oui** (ombres de feuilles) |
| 6. Mots empilés | `mots.html` | `mot1` à `mot4`, `texte` | Comprendre | non |
| 7. Photo en arche | `arche.html` | `label`, `titre` (une ligne), `photo`, `cadrage`, `texte` | Coulisses, Pour qui | non |
| 8. Aquarelle | `couverture.html`, `diapo.html`, `story.html` | `titre`, `sous_titre`, `texte`, `variante` | tous | **oui**, sauf `variante` `creme`, `tendre` ou `foret` |
| Dernière diapo | `fin.html` | `titre`, `texte` (rappel médical inclus) | tous | non |

- **Photos** : celles de la salle d'Enza sont dans `a-deposer\salle-enza\` (piano, bols chantants, ukulélé, plantes, sans visage). `cadrage` règle la partie visible de la photo, par exemple `50% 40%` (horizontal, vertical). Vérifier qu'aucune étiquette, aucun câble ou objet personnel ne gêne.
- **Fond IA** : un post est déclaré `isAiGenerated: true` dès qu'**une** de ses images montre un fond IA (aquarelle ou ombres de feuilles). Un carrousel fait seulement de visages « non » reste à `false`.
- **Grille du profil** : Instagram montre les posts recadrés en 3:4 (34 px coupés de chaque côté). La marge de 96 px protège le texte. Ne jamais placer un mot important près des bords.
- Calme, aéré, lisible sur un téléphone, accessible aux personnes âgées : texte courant à 44 px au moins sur une image de 1080 px de large, contraste confortable.
- Logo : uniquement les tracés exacts de `logo_Enza.svg` (racine du site).

## Les formats

| Format | Taille | Gabarit |
|---|---|---|
| Post, carrousel (10 images maximum) | **1080 × 1350** (4:5), JPEG | les 8 visages ci-dessus et `fin.html` |
| Story | **1080 × 1920** (9:16), JPEG | `story.html` (haut et bas laissés libres pour l'interface d'Instagram) |
| Reel | **1080 × 1920**, MP4 | plus tard (outil de montage pas encore installé) |

Chaque image a un **texte alternatif** (description courte de ce qu'on voit, pour les personnes malvoyantes). Chaque vidéo parlée est **sous-titrée**.

## Ce qui vient du vrai, ce qui peut venir de l'IA

- **Jamais le visage d'Enza.** Sa voix, ses mains et ses instruments : oui.
- **Du vrai d'abord** : photos et enregistrements d'Enza (dossier `a-deposer\`), photos et vidéos **libres de droits** (demander l'accord de l'utilisateur avant chaque téléchargement, noter la source dans le dossier du post).
- **IA acceptée si discrète** : fonds, textures, lumière, illustrations douces, plans d'ambiance (eau, forêt, lumière).
- **Jamais confié à l'IA** : mains, instruments, visages, texte dans l'image. Ces éléments viennent de vraies photos ; le texte est toujours posé par les gabarits.
- **Jamais** : fausses personnes réalistes, faux patients, fausses séances, faux témoignages.
- Tout contenu créé ou nettement modifié par IA est **déclaré** : `isAiGenerated: true` dans `instagramData` (voir `metricool.md`).
- Le skill doit fonctionner **sans** générateur d'images : typographie, photos d'Enza, photos libres de droits. L'IA reste un complément.
- **Générateur branché : Higgsfield** (connecteur « le Higgsfield »), plan gratuit, environ 10 crédits. Annoncer le coût à l'utilisateur avant de générer (`balance`, puis `get_cost: true`). Sur ce plan, le modèle utilisable est `z_image` (0,15 crédit, format 3:4) ; `gpt_image_2_5` demande un abonnement payant. Il arrive que `z_image` refuse une image de plus quand on en envoie plusieurs d'un coup (limite de débit) : relancer cette image seule.
- Un fond IA sort souvent vert menthe : le **recolorer** dans le vert du thème (niveaux de gris, puis `ImageOps.colorize` autour de `--fond`) et le recadrer en 4:5 (`ImageOps.fit`) avant de le passer à `rendre(..., {"fond": ...})`.

## La musique

Uniquement les **enregistrements d'Enza** ou des **sons libres de droits**. Jamais de musique du commerce.

## Contrôle qualité (chaque image, en taille réelle, avant de la montrer)

- [ ] Aucun texte coupé, collé au bord ou trop petit pour un téléphone.
- [ ] Orthographe, accents et typographie française corrects.
- [ ] Aucun défaut d'IA : doigts, cordes, touches, objets impossibles, textures qui fondent.
- [ ] Rien qui fasse « artificiel », criard ou racoleur ; couleurs dans la palette.
- [ ] Cohérent avec les autres posts et les `references-style\`.
- [ ] Aucune personne reconnaissable sans accord écrit, jamais le visage d'Enza.
- [ ] Le visuel dit la même chose que la légende.

Au moindre doute, on écarte l'image : une belle photo libre de droits vaut mieux qu'une image IA moyenne.

## Le test de style

1. Rendre une planche de 4 à 6 variantes de couverture : police des titres, nuance de vert, avec ou sans plante.
2. Si l'utilisateur a activé un générateur d'images, ajouter des variantes avec des fonds IA discrets.
3. Enza choisit. Reporter son choix dans `theme.css`, copier les visuels retenus dans `references-style\`.

Fait le 8 novembre 2026 : variante B retenue (planche dans `posts\2026-11-10-test-de-style\`). Quatre fonds IA discrets ont ensuite été testés dans ce style (`posts\2026-11-10-test-de-style\fonds-ia\`). Enza a choisi **B4, l'aquarelle**. Le même jour, l'utilisateur a jugé les posts trop semblables : les 8 visages ont été adoptés (planche dans `posts\propositions-variete\`), et l'aquarelle n'est plus que l'un d'eux.
