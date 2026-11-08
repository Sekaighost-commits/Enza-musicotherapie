# Skill « Instagram d'Enza » — Design

**Date** : 2026-11-08
**Statut** : validé en conversation, à relire par l'utilisateur
**Type** : skill Claude Code propre au projet (pas une page du site)

## Intention

Enza Duhem (musicothérapeute **en formation**, Vaulx/Tournai) a un compte Instagram professionnel, `@musicotherapienza`, avec seulement 4 posts. L'utilisateur, qui gère le site et les supports d'Enza, veut un skill qui l'aide à faire vivre ce compte **dans la logique du projet** :

- **vulgariser** la musicothérapie et **informer** le plus de monde possible ;
- créer une **safe place** : un compte rassurant et digne de confiance ;
- **amener à réserver** séances, ateliers et stages, en douceur.

Il ne s'agit **pas** de devenir influenceuse. Le public, le ton et ce qu'il faut éviter sont déjà décrits dans `PRODUCT.md` (section Users, Brand Personality, Anti-references) : le skill s'y réfère au lieu de les recopier, et on ne les redemande pas à l'utilisateur.

## Objectifs, non-objectifs, anti-objectifs

**Objectifs**
- Tenir **2 à 3 posts par semaine** sur Instagram, repris sur la page Facebook d'Enza.
- Que chaque post soit préparé par l'utilisateur avec Claude, **validé par Enza**, puis programmé.
- Mesurer le succès par les **demandes de contact venues d'Instagram**, pas par les abonnés ou les vues.

**Non-objectifs**
- Répondre aux commentaires ou aux messages privés à la place d'Enza (elle répond elle-même ; le skill prépare des réponses types).
- Publicité payante, « boost », achat d'abonnés, prospection en messages privés.
- Autres réseaux que Instagram et Facebook.

**Anti-objectifs** (échec même si « ça marche »)
- Un ton d'influenceuse : accroches choc, viralité, fausses urgences, promos criardes.
- Des images IA qui se voient : mains déformées, instruments impossibles, texte déformé, couleurs criardes. Une image moyenne rebute ; elle n'est jamais publiée.
- Une promesse de guérison, un sujet trop intime, une confusion avec un avis médical.
- Présenter Enza comme diplômée (elle est **en formation**).

## Ce qui a été décidé avec l'utilisateur

### Rôles
- L'**utilisateur** prépare les posts avec Claude.
- **Enza valide** chaque post. Rien n'est programmé sans son accord, transmis par l'utilisateur.

### Présence d'Enza
- **Jamais son visage.**
- Sa **voix**, ses **mains** et ses **instruments** : oui.

### Formats
Variés, pas seulement de la vidéo, et une vidéo ne la montre pas forcément :
- carrousels pédagogiques ;
- images seules (idée clé, résultat de recherche, phrase forte) ;
- vidéos courtes sans Enza à l'écran (nature, instruments, texte animé, illustrations) avec sa voix ou ses sons ;
- vidéos « mains et instruments » filmées par Enza quand elle en a l'envie ;
- stories pour les infos pratiques (dates d'ateliers, places, nouvel article).

### Musique
Uniquement les **enregistrements d'Enza** ou des **sons libres de droits**. Jamais de musique du commerce.

### Facebook
Chaque post part aussi sur la page Facebook d'Enza (déjà reliée à Metricool). L'utilisateur n'a rien à adapter : le skill s'occupe des différences entre les réseaux.

### Visuels et IA
- **Base** : le style des posts actuels (fond vert pâle, plante, gros titre crème).
- **Du vrai d'abord** : mains et instruments d'Enza, ses enregistrements, photos et vidéos libres de droits.
- **IA acceptée si discrète** : fonds, textures, lumière, illustrations douces, plans d'ambiance.
- **Jamais confié à l'IA** : mains, instruments, visages, texte dans l'image. Ces éléments viennent de vraies photos ; le texte est toujours posé par Claude, avec les polices et couleurs d'Enza.
- **Jamais** : fausses personnes réalistes, faux patients, fausses séances, faux témoignages.
- Contenu IA **toujours déclaré** à Instagram (`isAiGenerated`), comme la règle l'exige.
- **Contrôle qualité** de chaque visuel en taille réelle avant de le montrer. Au moindre doute, on l'écarte.
- **Test de style au départ** : une petite série générée ; Enza garde celles qui lui plaisent, elles deviennent les références des images suivantes. L'outil de génération est choisi à ce moment-là (un connecteur de génération d'images existe dans la configuration mais est désactivé). **Le skill doit fonctionner sans générateur IA** (typographie, photos d'Enza, photos libres de droits) : l'IA est un complément, pas une dépendance.

### Règles de contenu
- **Aucune promesse de guérison.** Vocabulaire : « accompagner », « soutenir », « apaiser », « aider à exprimer ». Interdits : « guérir », « soigner », « traiter », « efficace contre », « miracle ».
- **Rien de trop intime.** Pas de récits de séances ni de cas, même anonymes. Les sujets lourds (deuil, fin de vie, burn-out) sont abordés de façon générale et avec douceur.
- **Rappel obligatoire** dans chaque post qui parle de santé ou de difficultés : « La musicothérapie accompagne, elle ne remplace pas l'avis d'un médecin ou d'un spécialiste. » (formulation adaptable, sens intangible). Le même rappel figure dans la bio.
- **Statut** : toujours « musicothérapeute en formation ».
- **Personnes** : aucun enfant ni patient reconnaissable sans accord écrit ; aucun faux témoignage.
- **Recherche** : résumée honnêtement, source citée, jamais exagérée.
- **Personne en détresse** : réponse type chaleureuse pour Enza, qui oriente vers le **112**, le **Centre de Prévention du Suicide (0800 32 123)** et **Télé-Accueil (107)**.

### Thèmes (≈ 10 à 12 posts par mois)
| Thème | Part | Contenu |
|---|---|---|
| Comprendre | ≈ 4/10 | idées reçues (« faut-il être musicien ? »), déroulé d'une séance, différence avec un cours de musique ou une playlist relaxante |
| Pour qui | ≈ 2-3/10 | un domaine à la fois (périnatalité, enfance, adultes, personnes âgées, soins palliatifs), avec renvoi vers l'article du site |
| Ce que dit la recherche | ≈ 1/10 | un résultat d'étude expliqué simplement, avec sa source |
| Une pause pour soi | ≈ 1-2/10 | petits exercices de bien-être à essayer chez soi, « pause sonore » enregistrée par Enza ; présentés comme du bien-être, jamais comme une thérapie |
| Coulisses et actu | ≈ 1/10 | instruments (mains), formation, ateliers à venir, stages |

**Invitation à réserver** : chaque post se termine en douceur (« Pour en parler, le lien est dans la bio »). Environ un post sur trois invite plus clairement à prendre contact, sans presser.

### Déroulé
1. **« Prépare la semaine »** : Claude consulte le journal des posts, propose 2 ou 3 sujets en équilibrant les thèmes ; l'utilisateur choisit.
2. **Fabrication** : visuels + texte, contrôle qualité, aperçu montré à l'utilisateur.
3. **Brouillons Metricool** : dépôt en brouillon (rien de public). Enza se connecte elle-même à Metricool sur son téléphone (confirmé par l'utilisateur) et voit les brouillons tels qu'ils paraîtront ; s'il y a des corrections, Claude les applique.
4. **« Enza a validé »** : Claude programme **ce post-là** à la meilleure heure (`getBestTimeToPostByNetwork`). Jamais de programmation sans cette phrase de l'utilisateur pour le post concerné.
5. **« Bilan du mois »** : statistiques Metricool + demandes de contact venues d'Instagram ; propositions d'ajustement des thèmes. Les demandes arrivent dans Notion (champs « Découvert via » et « Source auto ») : tant que Notion n'est pas relié à Claude, l'utilisateur donne ces chiffres.

**En plus**
- **Réponses types** pour Enza : tarifs, réservation, question médicale (« je ne peux pas donner d'avis médical »), demande de professionnel, personne en détresse.
- **Bio** : texte proposé (rappel « ne remplace pas » + lien `https://musicotherapeute-hainaut.be/?utm_source=instagram`). Enza le colle elle-même : Metricool ne modifie pas les bios. Même logique pour Facebook avec `?utm_source=facebook`.
- **Matière d'Enza** (photos de mains/instruments, enregistrements) : elle l'envoie à l'utilisateur, qui la dépose dans un dossier prévu.
- **Premier lot** : une version corrigée du flyer (atelier collectif **1 h 30**, 15 €/pers. ; le flyer actuel indique encore « 15 €/pers./h »), et le test de style.

## Contraintes techniques connues

- **Metricool** : connecteur branché. Marque `musicotherapienza`, page Facebook liée, fuseau `Europe/Paris` (l'identifiant de marque s'obtient avec `getBrandSettings`). Plan **gratuit** : environ 20 publications programmées par mois ; l'envoi « pour validation » intégré (`createScheduledPostForReview`) exige un plan avec gestion d'équipe, donc la validation passe par les **brouillons** (`draft: true`), puis `updateScheduledPost` (`draft: false`).
- **Un seul post Metricool pour les deux réseaux** quand c'est possible, pour ne pas doubler le décompte : un texte commun (adresse du site écrite en clair, cliquable sur Facebook, lisible sur Instagram ; hashtags peu nombreux, sans gêne sur Facebook). Deux posts séparés seulement si le texte doit vraiment différer.
- **Médias** : Metricool exige des **URL publiques**. Les visuels sont publiés dans un dossier du site non lié et exclu des moteurs (`robots.txt`), puis retirés une fois le post publié.
- **Formats** : posts et carrousels 1080 × 1350 (4:5), reels et stories 1080 × 1920 (9:16). Vidéos sous-titrées (beaucoup regardent sans le son, et pour l'accessibilité). Texte alternatif sur chaque image (`mediaAltText`).
- **Légende Instagram** : environ 125 caractères visibles avant « … plus » ; les liens n'y sont pas cliquables ; nombre de hashtags limité (vérifier la limite en vigueur).
- **Typographie française** respectée : espaces insécables avant « : ; ! ? », guillemets « ».
- **Téléchargements** (photos/vidéos libres de droits) : Claude demande l'accord de l'utilisateur avant chacun.
- **Toujours en français** dans les échanges avec l'utilisateur.

## Laissé au constructeur

- Structure interne du skill (un `SKILL.md` + fichiers de référence + petits scripts), noms des fichiers, déclencheurs.
- Outils de rendu des visuels (HTML → PNG, comme pour les fiches PDF du projet) et de montage vidéo (vérifier ce qui est installé).
- Un vérificateur de légende (aperçu des 125 caractères, mots interdits, présence du rappel, nombre de hashtags). Les idées du dépôt MIT `jakeschincariol/instagram-agent-skill` peuvent inspirer, mais rien n'est repris tel quel : il est anglophone, il casse la typographie française et son esprit est « viral ».
- Format du journal des posts.
- Choix des hashtags (locaux + thème, en français).

## Choix faits par Claude (à vérifier par l'utilisateur)

- Emplacement du skill : `.claude/skills/instagram-enza/` dans le dépôt, versionné avec le projet.
- Dossier de travail (matière d'Enza, visuels, aperçus, journal) **hors du dépôt**, à un chemin fixe partagé par toutes les sessions : `C:\Users\Sekai\Documents\Instagram-Enza\`.
- Dossier public des médias : `medias-instagram/` à la racine du site, exclu dans `robots.txt`.
- Si Metricool est un jour indisponible pour Enza, l'aperçu lui est envoyé par l'utilisateur (image de chaque post) ; la règle « rien sans son accord » ne change pas.
- La formulation exacte du rappel « ne remplace pas » et du texte de bio est proposée par Claude, validée par Enza au premier lot.
