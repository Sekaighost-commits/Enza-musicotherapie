# Règles de contenu

Ces règles valent pour chaque légende, chaque visuel et chaque réponse préparée. Le ton (confiant, chaleureux, doux, sans jargon) est décrit dans `PRODUCT.md`.

## 1. Aucune promesse de guérison

| On écrit | On n'écrit jamais |
|---|---|
| accompagner, soutenir, apaiser, aider à exprimer, offrir un espace, peut aider à | guérir, guérison, soigner, traiter, efficace contre, miracle |

« Soins palliatifs » et « traitement » (dans le rappel médical) restent permis. `scripts/legende.py` bloque les mots interdits.

## 2. Rien de trop intime

- Pas de récit de séance ni de cas, même anonyme, même « inspiré de ».
- Les sujets lourds (deuil, fin de vie, burn-out, troubles chez l'enfant) sont abordés **de façon générale et avec douceur**, jamais en détail ni de façon dramatique.
- Pas de détail sur la vie privée d'Enza au-delà de ce qu'elle a choisi de dire (« Mon histoire »).

## 3. Le rappel médical

Dans **chaque post qui parle de santé ou de difficultés**, une phrase de ce sens (la formulation peut s'adapter, pas le sens) :

> La musicothérapie accompagne, elle ne remplace pas l'avis d'un médecin ou d'un spécialiste.

Le même rappel figure dans la bio. Pour vérifier une légende de ce type : `python scripts/legende.py legende.txt --sante`.

## 4. Le statut d'Enza

Toujours « **musicothérapeute en formation** », comme sur le site. Jamais « musicothérapeute diplômée » ni « thérapeute certifiée ».

## 5. Les personnes

- Jamais le visage d'Enza.
- Aucun enfant ni patient reconnaissable sans **accord écrit** (parents pour un enfant). Dans le doute : on ne montre pas.
- Aucun faux témoignage, aucune fausse personne réaliste. Un vrai témoignage n'est utilisé qu'avec l'accord écrit de la personne, et un prénom modifié si elle le souhaite.

## 6. La recherche

- Un résultat d'étude est **résumé honnêtement**, avec sa source (auteurs ou organisme, année), et sans exagération : « une revue d'études suggère que… », jamais « la science prouve que… ».
- Les sources sérieuses déjà citées sur le site (page Professionnels, articles) sont un bon point de départ.

## 7. L'invitation à réserver

Chaque post se termine en douceur (« Pour en parler, le lien est dans la bio »). Environ un post sur trois invite plus clairement à prendre contact. **Jamais** de fausse urgence (« dernière chance », « plus que 2 places ! », « offre limitée »).

## 8. Une personne en détresse

Un compte qui parle de deuil ou d'anxiété peut recevoir un message inquiétant (idées noires, danger immédiat). Enza répond elle-même, en partant de la réponse type de `reponses-types.md`, qui oriente vers :

- le **112** en cas d'urgence ;
- le **Centre de Prévention du Suicide : 0800 32 123** (gratuit, 24 h/24) ;
- **Télé-Accueil : 107** (gratuit, anonyme, 24 h/24).

Ce message passe avant tout le reste.

## 9. Forme

- Typographie française : espace insécable avant « : ; ! ? », guillemets « ».
- Hashtags : **5 au maximum**, légende et commentaires compris (règle d'Instagram depuis décembre 2025). En français, locaux et de thème, par exemple #musicothérapie #tournai #hainaut #wallonie. Pas de mur de hashtags.
- L'adresse du site s'écrit en clair (`musicotherapeute-hainaut.be`) : cliquable sur Facebook, lisible sur Instagram.
- Le début de la légende compte : environ **125 caractères** sont visibles avant « … plus ».
