# Procédure Metricool

Metricool est relié au compte Instagram `@musicotherapienza` et à la page Facebook d'Enza. Claude le pilote avec les outils du connecteur Metricool.

## Repères

- `getBrandSettings` : donne le **blogId** de la marque `musicotherapienza` et son fuseau horaire (`Europe/Paris`, même heure que la Belgique). Le relire à chaque session plutôt que de le recopier.
- **Plan gratuit** : environ 20 publications programmées par mois. L'envoi « pour validation » (`createScheduledPostForReview`, `sendScheduledPostForReview`) exige un plan payant : on passe par les **brouillons**.
- **Un seul post pour les deux réseaux** (providers instagram + facebook, texte commun) afin de ne compter qu'une fois. Deux posts séparés seulement si le texte doit vraiment différer.
- Hashtags : 5 au maximum, légende **et** premier commentaire compris : ne pas en ajouter dans `firstCommentText`.
- Les dates sont toujours dans le futur. Le paramètre `date` est en ISO 8601 avec décalage (`2026-11-12T18:00:00+01:00` en hiver, `+02:00` en été).

## 1. Mettre les médias en ligne

```python
from medias import preparer, attendre_en_ligne
urls = preparer([...chemins des JPEG dans l'ordre...], "2026-11-12-faut-il-etre-musicien")
```

Puis déployer le site (commit de `medias-instagram/<lot>/`, fusion rapide dans `master`, push), puis :

```python
attendre_en_ligne(urls)   # True quand toutes les images répondent ; sinon NE PAS créer le brouillon
```

## 2. Créer le brouillon

`createScheduledPost` avec `blogId`, `date` (date prévue) et `info` :

```json
{
  "text": "Légende vérifiée par legende.py",
  "providers": [{"network": "instagram"}, {"network": "facebook"}],
  "publicationDate": {"dateTime": "2026-11-12T18:00:00", "timezone": "Europe/Paris"},
  "draft": true,
  "autoPublish": true,
  "media": ["https://musicotherapeute-hainaut.be/medias-instagram/2026-11-12-faut-il-etre-musicien/01-couverture.jpg"],
  "mediaAltText": ["Texte alternatif de l'image 1"],
  "firstCommentText": "",
  "shortener": false,
  "smartLinkData": {"ids": []},
  "descendants": [],
  "hasNotReadNotes": false,
  "instagramData": {"type": "POST", "showReelOnFeed": true, "isAiGenerated": true},
  "facebookData": {"type": "POST"}
}
```

- Carrousel : plusieurs URL dans `media` (10 au maximum), un texte alternatif par image, dans le même ordre.
- **Story** : `instagramData.type` et `facebookData.type` à `"STORY"`, une seule image 1080 × 1920, et **pas de texte** (une story n'a pas de légende).
- `isAiGenerated: true` dès qu'une image a été créée ou nettement modifiée par IA. C'est le cas du **fond aquarelle par défaut** des gabarits : tout post fait avec `couverture.html`, `diapo.html` ou `story.html` sans photo dans le champ `fond` est donc à `true`. `false` seulement si aucune image du post ne contient d'IA (par exemple vraies photos seules, ou flyer).
- Noter dans le journal l'**uuid** renvoyé et l'adresse du post dans Metricool (`plannerUrl`).

**Après le brouillon** : relire le post avec `getScheduledPosts` (même période, `timezone: "Europe/Paris"`) et vérifier qu'il est **toujours en brouillon** (`"draft": true`). Sinon, le repasser immédiatement en brouillon avec `updateScheduledPost` et prévenir l'utilisateur. Si les adresses des médias pointent vers Metricool (`static.metricool.com/...`) et plus vers `musicotherapeute-hainaut.be`, Metricool a gardé sa copie : retirer tout de suite les médias du site (`medias.retirer(lot)` puis déploiement). Sinon, attendre la publication.
**Constat du premier brouillon (8 novembre 2026)** : Metricool copie les médias **dès la création du brouillon**. Les images ne restent donc en ligne sur le site que quelques minutes.

## 3. Programmer après « Enza a validé »

1. `getBestTimeToPostByNetwork` (`socialNetwork: "instagram"`, sur le jour prévu ou la semaine) : choisir le meilleur créneau.
2. `getScheduledPosts` pour récupérer l'`id`, l'`uuid` et **tout** le contenu du brouillon.
3. `updateScheduledPost` (`id`, `uuid`, `blogId`, `info`) avec le contenu complet inchangé, sauf `draft: false` et la nouvelle date dans `info.publicationDate`. Attention : `updateScheduledPost` n'a pas de paramètre `date` (contrairement à `createScheduledPost`). La mise à jour change l'`id`, garder l'`uuid`.
4. Annoncer à l'utilisateur la date et l'heure. Journal : `programmé`.

Une correction demandée par Enza se fait aussi avec `updateScheduledPost`, en écrivant explicitement `"draft": true` dans `info` (la valeur par défaut est `false` : l'oublier programmerait le post). Relire ensuite avec `getScheduledPosts` : le post doit être **toujours en brouillon**. Puis on attend une nouvelle validation. Pour un visuel corrigé, utiliser un nouveau nom de lot (par exemple `…-v2`) : le cache du site peut servir l'ancienne image pendant 10 minutes.

## 4. Bilan du mois

- `getAnalyticsAvailableMetrics` (`network: "instagram"`, puis `"facebook"`, connecteur `posts`) pour connaître les métriques disponibles.
- `getAnalyticsDataByMetrics` (`brandId`, du 1er au dernier jour du mois) avec les métriques utiles : portée, enregistrements, partages, visites du profil, clics sur le lien.
- Croiser avec le nombre de demandes de contact venues d'Instagram et de Facebook, que l'utilisateur lit dans Notion.

## Limites

- Metricool ne modifie pas la bio et ne supprime pas un post déjà publié : Enza le fait dans l'app Instagram (par exemple archiver l'ancien flyer).
- Metricool ne gère ni les commentaires ni les messages privés via Claude.
