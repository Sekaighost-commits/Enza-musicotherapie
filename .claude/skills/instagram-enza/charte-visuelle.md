# Charte visuelle

## Le style

- **Style retenu par Enza (test de style du 8 novembre 2026) : variante B, « proche des posts actuels ».** Fond vert tendre, grand titre crème en police bâton étroite (Oswald) avec une ombre verte, texte en DM Sans. Les titres des diapos intérieures sont en vert foncé, pour rester lisibles. La dernière diapo est en vert feuille foncé avec le texte en crème. Référence : `references-style\variante-B.jpg` dans le dossier de travail.
- Polices et couleurs vivent dans `gabarits/theme.css` : c'est le **seul** fichier à modifier si le style évolue. Les gabarits (`couverture.html`, `diapo.html`, `fin.html`, `story.html`) n'ont pas à changer.
- Calme, aéré, lisible sur un téléphone, accessible aux personnes âgées : texte courant à 44 px au moins sur une image de 1080 px de large, contraste confortable.
- Logo : uniquement les tracés exacts de `logo_Enza.svg` (racine du site).

## Les formats

| Format | Taille | Gabarit |
|---|---|---|
| Post, carrousel (10 images maximum) | **1080 × 1350** (4:5), JPEG | `couverture.html`, `diapo.html`, `fin.html` |
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

Fait le 8 novembre 2026 : variante B retenue (planche dans `posts\2026-11-10-test-de-style\`). Les fonds IA discrets restent à tester dans ce style quand le générateur d'images sera utilisable.
