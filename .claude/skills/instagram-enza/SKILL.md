---
name: instagram-enza
description: Gérer le compte Instagram @musicotherapienza et la page Facebook d'Enza Duhem, musicothérapeute en formation (Vaulx, Tournai) - préparer les posts (carrousels, images, stories), les déposer en brouillon dans Metricool, les programmer après validation d'Enza, faire le bilan du mois, préparer des réponses types et la bio. À utiliser quand l'utilisateur dit « prépare la semaine », « Enza a validé », « bilan du mois », ou parle de posts, carrousel, story, reel, Instagram, Facebook ou Metricool.
---

# Instagram d'Enza

Toujours répondre **en français** à l'utilisateur.

## Pourquoi ce compte existe

Vulgariser la musicothérapie, informer le plus de monde possible, créer une **safe place** et amener à réserver séances, ateliers et stages, **en douceur**. Ce n'est pas un compte d'influenceuse.
Public, ton et anti-références : lire `PRODUCT.md` à la racine du site. Ne pas les redemander à l'utilisateur.

## Rôles

- **L'utilisateur** prépare les posts avec Claude.
- **Enza** valide chaque post, dans l'app Metricool sur son téléphone.
- **Claude** ne programme un post qu'après la phrase « Enza a validé » pour **ce** post.

## Règles d'or (sans exception)

1. **Rien n'est programmé sans « Enza a validé »** pour le post concerné. Avant cela, le post reste en brouillon (`draft: true`), invisible du public.
2. **Jamais le visage d'Enza.** Sa voix, ses mains et ses instruments : oui.
3. Chaque légende respecte `regles-contenu.md` et passe `scripts/legende.py` sans aucun BLOQUANT.
4. Chaque visuel respecte `charte-visuelle.md` et passe le contrôle qualité **en taille réelle** avant d'être montré. Au moindre doute, on l'écarte.
5. Télécharger une photo, une vidéo ou un son libre de droits : **demander l'accord de l'utilisateur avant chacun**.
6. Ne jamais répondre aux commentaires ni aux messages privés à la place d'Enza : préparer des réponses (`reponses-types.md`), c'est elle qui envoie.
7. **Après chaque écriture dans Metricool** qui doit laisser un brouillon (création, correction) : relire le post avec `getScheduledPosts` et vérifier qu'il est **toujours en brouillon** (`draft: true`). Sinon, le repasser immédiatement en brouillon et prévenir l'utilisateur.

## Fichiers

| Fichier | Contenu |
|---|---|
| `regles-contenu.md` | promesses interdites, sujets intimes, rappel médical, statut, personnes, recherche, détresse |
| `themes.md` | les 5 thèmes, leur part, la réserve de sujets, l'invitation à réserver |
| `charte-visuelle.md` | style, formats, vrai / IA, contrôle qualité, test de style, musique |
| `metricool.md` | procédure technique : brouillon, validation, statistiques |
| `reponses-types.md` | réponses pour Enza et textes de bio |
| `scripts/legende.py` | vérificateur de légende (`python scripts/legende.py legende.txt [--sante]`) |
| `scripts/visuel.py` | rendu des visuels (`rendre`, `rendre_carrousel`) à partir de `gabarits/` |
| `scripts/medias.py` | mise en ligne des médias (`preparer`, `attendre_en_ligne`, `retirer`) |
| `gabarits/` | les 8 visages (`photo`, `idee-recue`, `chiffre`, `citation`, `etapes`, `mots`, `arche`, aquarelle) + `gabarits/fin.html` ; `gabarits/theme.css` : polices, couleurs et mises en page |

**Dossier de travail** (hors du site, le même pour toutes les sessions) : `C:\Users\Sekai\Documents\Instagram-Enza\`
- `a-deposer\` : photos, vidéos et enregistrements envoyés par Enza ;
- `posts\AAAA-MM-JJ-sujet\` : un dossier par post (visuels, `legende.txt`, textes alternatifs) ;
- `references-style\` : visuels choisis par Enza au test de style ;
- `journal.md` : un tableau `| date prévue | thème | sujet | format | statut | uuid Metricool | lot médias |`, statuts `proposé`, `brouillon`, `validé`, `programmé`, `publié`, `refusé`.

S'il manque, créer ce dossier et ses sous-dossiers, et `journal.md` avec l'en-tête du tableau.

## « Prépare la semaine »

1. Lire `journal.md` et `themes.md`.
2. Proposer **2 ou 3 sujets** : pour chacun, le thème, le format, le **visage** (`charte-visuelle.md`) et l'idée en une phrase. Respecter les parts des thèmes sur les 12 derniers posts, éviter un sujet traité récemment, et faire inviter plus clairement à prendre contact environ un post sur trois. **Varier** : jamais deux posts de suite avec le même visage, en alternant clair, foncé et photo. Au moindre doute sur la variété, montrer une planche des couvertures prévues à côté des derniers posts. L'utilisateur choisit. Journal : `proposé`.
3. Pour chaque post retenu, créer `posts\AAAA-MM-JJ-sujet\` et écrire `legende.txt`, puis lancer `python scripts/legende.py legende.txt` (ajouter `--sante` si le post parle de santé ou de difficultés). Corriger jusqu'à **zéro BLOQUANT**, et examiner chaque ATTENTION.
4. Fabriquer les visuels avec `scripts/visuel.py` (`rendre` ou `rendre_carrousel`), avec le gabarit du visage choisi, en variant aussi les diapos d'un carrousel. En cas de `DebordementTexte`, raccourcir le texte, ne jamais réduire la police jusqu'à l'illisible. En cas de `PoliceManquante`, vérifier la connexion.
5. **Contrôle qualité** de chaque image en taille réelle (liste dans `charte-visuelle.md`), puis écrire un texte alternatif par image.
6. Montrer à l'utilisateur les images, la légende et les textes alternatifs, et corriger s'il le demande.
7. Déposer le **brouillon** dans Metricool en suivant `metricool.md`, vérifier qu'il apparaît **toujours en brouillon**, puis, si Metricool en a gardé une copie (adresses `static.metricool.com`), retirer les médias du site. Journal : `brouillon`.
8. Dire à l'utilisateur qu'Enza peut regarder les brouillons dans l'app Metricool. Si Metricool lui est inaccessible, l'utilisateur lui envoie les images.

## « Enza a validé »

1. Identifier le post concerné à partir du journal et de `getScheduledPosts`. Si plusieurs brouillons sont possibles, demander lequel : la validation vaut pour **un** post précis.
2. Choisir l'heure avec `getBestTimeToPostByNetwork` autour de la date prévue, puis passer le brouillon en programmé (`metricool.md`). Annoncer à l'utilisateur la date et l'heure. Journal : `programmé`.
3. Si Enza demande une correction, corriger, mettre à jour le brouillon, vérifier qu'il est toujours en brouillon (règle d'or 7) et attendre une nouvelle validation.
4. Vérifier que les médias ne sont plus sur le site (ils ont dû être retirés après le brouillon, voir `metricool.md`).

## « Bilan du mois »

1. Récupérer les statistiques Instagram et Facebook du mois dans Metricool (`metricool.md`).
2. Demander à l'utilisateur le nombre de demandes de contact venues d'Instagram et de Facebook. Elles arrivent dans Notion (champs « Découvert via » et « Source auto »), que Claude ne lit pas.
3. Résumer en quelques lignes ce qui a le mieux marché : partages, enregistrements, visites du profil et surtout **demandes de contact**, pas seulement les « j'aime ». Proposer un ajustement des thèmes si besoin. Journal : passer en `publié` les posts parus.

## Réponses types et bio

- Un message ou un commentaire à traiter : partir de `reponses-types.md` et adapter. Une **personne en détresse** passe toujours en premier.
- La bio : textes prêts dans `reponses-types.md`. Enza les colle elle-même, car Metricool ne modifie pas les bios.

## Mettre les médias en ligne

Metricool n'accepte que des images en ligne. `medias.preparer(fichiers, lot)` copie les visuels dans `medias-instagram/<lot>/` à la racine du site. Il faut ensuite déployer le site avec le flux habituel (commit, fusion rapide dans `master`, push), puis attendre avec `medias.attendre_en_ligne(urls)` qu'ils répondent avant de créer le brouillon. `robots.txt` exclut ce dossier des moteurs de recherche.
