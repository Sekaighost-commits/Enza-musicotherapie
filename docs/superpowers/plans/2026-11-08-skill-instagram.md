# Skill « Instagram d'Enza » — Plan de construction

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal :** un skill Claude Code, propre au projet, qui aide l'utilisateur à préparer 2 à 3 posts par semaine pour Instagram et Facebook, à les déposer en brouillon dans Metricool, puis à les programmer après validation d'Enza.

**Architecture :** un `SKILL.md` qui porte le déroulé et renvoie vers cinq fichiers de référence (règles, thèmes, charte visuelle, procédure Metricool, réponses types), plus trois petits scripts Python testés : vérificateur de légende, rendu des visuels (HTML → JPEG via Playwright), mise en ligne des médias dans un dossier caché du site. Metricool est piloté par Claude via le connecteur MCP déjà branché, pas par un script.

**Tech Stack :** Python 3.14 (bibliothèque standard + `unittest`), Playwright/Chromium et Pillow (déjà installés), connecteur MCP Metricool, GitHub Pages (déploiement habituel). `pytest` et `ffmpeg` ne sont **pas** installés : on n'en dépend pas, sauf la tâche 7 (vidéo), conditionnelle.

**Spec :** `docs/superpowers/specs/2026-11-08-skill-instagram-design.md`

## Global Constraints

- Toujours répondre **en français** à l'utilisateur.
- Public, ton et anti-références : `PRODUCT.md` (on s'y réfère, on ne recopie pas, on ne redemande pas).
- **Jamais de programmation** d'un post sans la phrase de l'utilisateur « Enza a validé » pour **ce** post. Les brouillons (`draft: true`) ne sont pas publics.
- **Jamais le visage d'Enza.** Voix, mains et instruments : oui.
- Musique : uniquement les enregistrements d'Enza ou des sons libres de droits.
- Interdits : « guérir », « soigner », « traiter », « efficace contre », « miracle ». Vocabulaire : « accompagner », « soutenir », « apaiser », « aider à exprimer ».
- Rappel dans chaque post santé : « La musicothérapie accompagne, elle ne remplace pas l'avis d'un médecin ou d'un spécialiste. »
- Statut : toujours « musicothérapeute en formation ».
- Détresse : **112**, **Centre de Prévention du Suicide 0800 32 123**, **Télé-Accueil 107**.
- Pas de récit de séance ni de cas ; aucun enfant ni patient reconnaissable sans accord écrit ; aucun faux témoignage ; pas de fausses personnes réalistes.
- IA : jamais pour mains, instruments, visages, texte dans l'image ; contenu IA déclaré (`isAiGenerated: true`).
- Formats : post/carrousel **1080 × 1350**, story/reel **1080 × 1920** ; images en **JPEG** ; texte alternatif sur chaque image (`mediaAltText`).
- Un seul post Metricool pour Instagram + Facebook (texte commun, adresse du site écrite en clair) ; deux posts seulement si le texte doit vraiment différer. Plan gratuit : ≈ 20 publications programmées par mois.
- Médias publics dans `medias-instagram/` (exclu par `robots.txt`), retirés dès qu'ils ne sont plus nécessaires.
- Typographie française : espace (insécable) avant « : ; ! ? », guillemets « ».
- Téléchargement d'une photo ou vidéo libre de droits : accord de l'utilisateur avant **chacun**.
- Liens de bio : `https://musicotherapeute-hainaut.be/?utm_source=instagram` et `?utm_source=facebook`.
- Dossier de travail : `C:\Users\Sekai\Documents\Instagram-Enza\` (hors dépôt).
- Tarifs et coordonnées (charte) : séance individuelle 50 € (60 min, à domicile) ; atelier collectif 15 €/pers. (4 à 12 pers., **1 h 30**, à Vaulx ou à domicile) ; pack découverte 135 € (3 séances individuelles) ; interventions en institution, école, autres : sur demande. « Vaulx, Tournai (Hainaut), Belgique » sans code postal ; « (+32) 0496/35.01.37 » ; enza@musicotherapeute-hainaut.be. Logo : tracés exacts de `logo_Enza.svg`.
- Tests : `python -m unittest discover -s .claude/skills/instagram-enza/tests -v`, lancé depuis la racine du dépôt.

## Review Focus

1. **Accents « décomposés »** (texte collé depuis un téléphone, « gue\u0301rir ») : le vérificateur doit quand même bloquer → normaliser en NFC avant tout contrôle (tâche 1).
2. **Titre ou texte trop long dans un visuel** : il ne doit jamais être coupé au bord (déjà vécu avec les devis imprimés) → `rendre` lève `DebordementTexte` (tâche 2).
3. **Fichiers d'Enza aux noms avec espaces, accents, majuscules** (« Pause sonore été.JPG ») : URL propre et stable → `nom_web` (tâche 3).
4. **Image pas encore en ligne** juste après le déploiement (délai GitHub Pages + cache 10 min) : Metricool ne doit pas recevoir une URL en 404 → `attendre_en_ligne` avant tout brouillon (tâches 3 et 4).
5. **Hashtags accentués et émojis** (« #musicothérapie 🎶 ») : comptés correctement, sans compter « #1 » ni les ancres d'URL (tâche 1).

---

### Task 1 : Vérificateur de légende

**Files :**
- Create : `.claude/skills/instagram-enza/scripts/legende.py`
- Test : `.claude/skills/instagram-enza/tests/test_legende.py`

**Interfaces :**
- Produces :
  - `@dataclass(frozen=True) class Resultat: niveau: str; regle: str; message: str` — `niveau` ∈ `"BLOQUANT"`, `"ATTENTION"`.
  - `MAX_HASHTAGS: int`, `MAX_CARACTERES = 2200`, `APERCU = 125`.
  - `verifier(texte: str, sante: bool = False) -> list[Resultat]` (liste vide = tout va bien).
  - `apercu(texte: str) -> str` : les 125 premiers caractères, suivis de « … plus » si le texte est plus long.
  - CLI : `python legende.py <fichier.txt> [--sante]` affiche l'aperçu encadré puis chaque résultat ; code de sortie 1 s'il y a un `BLOQUANT`, sinon 0.

- [ ] **Step 1 : Vérifier la limite de hashtags en vigueur** (recherche web : la limite serait passée de 30 à 5 en décembre 2025). Noter la valeur et la source dans le docstring du module. Valeur par défaut si rien de fiable : 5.

- [ ] **Step 2 : Écrire les tests** (en tête de fichier : `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))`)

```python
RAPPEL = "La musicothérapie accompagne, elle ne remplace pas l'avis d'un médecin ou d'un spécialiste."
def regles(t, sante=False): return {r.regle for r in verifier(t, sante)}
def bloquants(t, sante=False): return {r.regle for r in verifier(t, sante) if r.niveau == "BLOQUANT"}

def test_promesse_bloquee(self):
    for t in ["La musique soigne l'anxiété.", "Elle peut guérir le stress.", "Un effet miracle.",
              "C'est efficace contre l'insomnie.", "On va traiter vos angoisses."]:
        self.assertIn("promesse", bloquants(t), t)
def test_soins_palliatifs_et_traitement_autorises(self):
    t = "En soins palliatifs, la musique apaise. " + RAPPEL + " Elle ne remplace pas un traitement."
    self.assertNotIn("promesse", regles(t, sante=True))
def test_accents_decomposes(self):   # Review Focus 1
    self.assertIn("promesse", bloquants("Pour gue\u0301rir vite."))
def test_rappel_obligatoire_si_sante(self):
    self.assertIn("rappel", bloquants("Le deuil se vit en musique.", sante=True))
    self.assertNotIn("rappel", regles("Le deuil se vit en musique. " + RAPPEL, sante=True))
    self.assertNotIn("rappel", regles("Atelier samedi à Vaulx.", sante=False))
def test_hashtags(self):              # Review Focus 5
    ok = "Texte 🎶 " + " ".join(f"#tag{i}" for i in range(MAX_HASHTAGS - 1)) + " #musicothérapie #1"
    self.assertNotIn("hashtags", regles(ok))
    trop = "Texte " + " ".join(f"#tag{i}" for i in range(MAX_HASHTAGS + 1))
    self.assertIn("hashtags", bloquants(trop))
def test_longueur(self):
    self.assertIn("longueur", bloquants("a" * 2201))
def test_attention_statut_lien_typo_urgence(self):
    self.assertIn("statut", regles("Enza, musicothérapeute à Tournai."))
    self.assertNotIn("statut", regles("Enza, musicothérapeute en formation à Tournai."))
    self.assertIn("lien", regles("Voir https://musicotherapeute-hainaut.be"))
    self.assertNotIn("lien", regles("Plus d'infos : musicotherapeute-hainaut.be"))
    self.assertIn("typographie", regles("Pour qui? Pour tous!"))
    self.assertNotIn("typographie", regles("Pour qui\u202f? Rendez-vous à 10:30."))
    self.assertIn("urgence", regles("Dernière chance, dépêchez-vous !!!"))
def test_apercu(self):
    self.assertEqual(apercu("Court."), "Court.")
    self.assertTrue(apercu("x" * 200).endswith("… plus"))
    self.assertEqual(len(apercu("x" * 200)), 125 + len("… plus"))
def test_cli_code_sortie(self):       # subprocess.run([sys.executable, LEGENDE_PY, fichier, ...])
    self.assertEqual(lancer("La musique soigne.").returncode, 1)
    self.assertEqual(lancer("Atelier à Vaulx. " + RAPPEL, "--sante").returncode, 0)
```

- [ ] **Step 3 : Lancer, vérifier l'échec** — `python -m unittest discover -s .claude/skills/instagram-enza/tests -v` → erreurs d'import (`legende` introuvable).

- [ ] **Step 4 : Implémenter `legende.py`.** Normaliser le texte en NFC d'abord. Règles :
  - `promesse` (BLOQUANT) : regex insensibles à la casse, avec limites de mot, sur les formes de « guérir/guérison », « soign(er|e|es|ent|ons|ez) » (pas « soins »), « trait(er|e|es|ent|ons|ez) » (pas « traitement »), « efficace contre », « miracle/miraculeu… ».
  - `rappel` (BLOQUANT si `sante`) : présence de « ne remplace pas » **et** de « médecin » ou « spécialiste ».
  - `hashtags` (BLOQUANT) : `#` précédé d'un début ou d'un espace et suivi d'au moins une lettre (accents compris) ; « #1 » n'en est pas un.
  - `longueur` (BLOQUANT) : > 2200 caractères.
  - `statut` (ATTENTION) : « musicothérapeute » sans « en formation » dans le texte.
  - `lien` (ATTENTION) : `http://` ou `https://` (non cliquable sur Instagram, écrire l'adresse en clair).
  - `typographie` (ATTENTION) : une lettre collée à « ? ! ; : », sauf `://` et les heures `\d:\d`.
  - `urgence` (ATTENTION) : « dernière chance », « offre limitée », « dépêchez », « !!! ».
  - `apercu_coupe` (ATTENTION) : la première phrase dépasse 125 caractères.

- [ ] **Step 5 : Relancer** → tous les tests de `test_legende` passent.

- [ ] **Step 6 : Commit** — `git add .claude/skills/instagram-enza && git commit -m "feat(instagram): vérificateur de légende (promesses, rappel, hashtags, typographie)"`

---

### Task 2 : Rendu des visuels

**Files :**
- Create : `.claude/skills/instagram-enza/scripts/visuel.py`
- Create : `.claude/skills/instagram-enza/gabarits/theme.css` (polices + couleurs en variables CSS : **seul fichier modifié par le test de style**)
- Create : `.claude/skills/instagram-enza/gabarits/couverture.html`, `diapo.html`, `fin.html`, `story.html`
- Test : `.claude/skills/instagram-enza/tests/test_visuel.py`

**Interfaces :**
- Produces :
  - `FORMATS = {"post": (1080, 1350), "story": (1080, 1920)}`
  - `class DebordementTexte(Exception)`, `class PoliceManquante(Exception)`
  - `rendre(gabarit: Path, champs: dict[str, str], sortie: Path, format: str = "post") -> Path` : remplit les `$cle` du gabarit (`string.Template.safe_substitute`, valeurs échappées en HTML sauf les chemins d'image, convertis en URI `file:///`), ouvre le HTML en `file://` dans Chromium à la taille exacte, attend `document.fonts.ready`, vérifie les polices, contrôle les débordements, enregistre en **JPEG** RGB qualité 90. Renvoie `sortie` (extension `.jpg` imposée).
  - Polices : `theme.css` déclare `--polices: "DM Sans", "<police des titres>"` sur `:root` ; chaque famille listée doit avoir dans `document.fonts` une police au statut `loaded`, sinon `PoliceManquante` (on ne publie jamais un visuel rendu avec une police de secours).
  - `rendre_carrousel(diapos: list[tuple[Path, dict[str, str]]], dossier: Path, format: str = "post") -> list[Path]` : `01.jpg`, `02.jpg`… ; `ValueError` au-delà de 10 diapos.
  - Convention des gabarits : chaque zone de texte porte l'attribut `data-cadre` ; champs utilisés : `titre`, `sous_titre`, `texte`, `fond` (image facultative), `pied` (adresse du site).

- [ ] **Step 1 : Écrire les tests**

```python
def test_taille_et_format(self):
    p = rendre(G / "couverture.html", {"titre": "Pour qui ?"}, tmp / "a.jpg")
    with Image.open(p) as im: self.assertEqual((im.size, im.format, im.mode), ((1080, 1350), "JPEG", "RGB"))
def test_story(self):
    p = rendre(G / "story.html", {"titre": "Atelier samedi"}, tmp / "s.jpg", format="story")
    with Image.open(p) as im: self.assertEqual(im.size, (1080, 1920))
def test_texte_trop_long(self):   # Review Focus 2
    with self.assertRaises(DebordementTexte):
        rendre(G / "couverture.html", {"titre": "Musicothérapie " * 40}, tmp / "b.jpg")
def test_echappement_html(self):
    rendre(G / "diapo.html", {"titre": "<b>«\u202fÀ deux\u202f»</b>", "texte": "Écoute & souffle"}, tmp / "c.jpg")  # aucune exception
def test_carrousel(self):
    ps = rendre_carrousel([(G / "couverture.html", {"titre": "1"}), (G / "fin.html", {"titre": "2"})], tmp)
    self.assertEqual([p.name for p in ps], ["01.jpg", "02.jpg"])
    with self.assertRaises(ValueError): rendre_carrousel([(G / "diapo.html", {})] * 11, tmp)
def test_police_manquante(self):  # gabarit temporaire avec <style>:root{--polices:"Police Inexistante"}</style>
    with self.assertRaises(PoliceManquante):
        rendre(gabarit_police_inexistante, {"titre": "Test"}, tmp / "d.jpg")
```

- [ ] **Step 2 : Lancer, vérifier l'échec** (import `visuel` introuvable).
- [ ] **Step 3 : Écrire `theme.css` et les 4 gabarits.** Point de départ = style des posts actuels : fond vert pâle, gros titre crème, plante (image `fond` facultative) ; texte courant en DM Sans, titres d'après la police retenue au test de style (en attendant : Cormorant Garamond). Polices chargées depuis Google Fonts. Marges intérieures ≥ 80 px. `fin.html` : invitation douce + `musicotherapeute-hainaut.be` + rappel « ne remplace pas ».
- [ ] **Step 4 : Implémenter `visuel.py`.** Débordement = pour chaque `[data-cadre]`, `scrollHeight > clientHeight + 1` ou `scrollWidth > clientWidth + 1`, ou rectangle hors de la fenêtre.
- [ ] **Step 5 : Relancer** → tests `test_visuel` OK (et `test_legende` toujours OK).
- [ ] **Step 6 : Contrôle visuel** : rendre une couverture et une diapo d'exemple dans le dossier temporaire et les regarder (Read de l'image) : rien de coupé, lisible sur téléphone.
- [ ] **Step 7 : Commit** — `feat(instagram): gabarits et rendu des visuels 1080×1350 / 1080×1920`

---

### Task 3 : Mise en ligne des médias

**Files :**
- Create : `.claude/skills/instagram-enza/scripts/medias.py`
- Modify : `robots.txt` (ajouter `Disallow: /medias-instagram/` après `Disallow: /confirmation.html`)
- Test : `.claude/skills/instagram-enza/tests/test_medias.py`

**Interfaces :**
- Produces :
  - `RACINE_SITE = Path(__file__).resolve().parents[4]`, `BASE_URL = "https://musicotherapeute-hainaut.be/medias-instagram/"`
  - `nom_web(nom: str) -> str`
  - `preparer(fichiers: list[Path], lot: str, racine: Path = RACINE_SITE) -> list[str]` : copie dans `<racine>/medias-instagram/<lot>/` sous le nom `NN-<nom_web>` (NN = position à partir de `01`, pour garder l'ordre du carrousel), renvoie les URL publiques **dans l'ordre**. `lot` doit respecter `^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$`. Extensions acceptées : `.jpg`, `.jpeg`, `.png`, `.mp4` ; image ≤ 8 Mo, vidéo ≤ 20 Mo ; sinon `ValueError` explicite (en français).
  - `retirer(lot: str, racine: Path = RACINE_SITE) -> None`
  - `attendre_en_ligne(urls: list[str], delai_max: int = 300, pas: int = 15) -> bool` : `True` quand toutes répondent 200.

- [ ] **Step 1 : Écrire les tests** (dossier temporaire comme `racine`)

```python
def test_nom_web(self):           # Review Focus 3
    self.assertEqual(nom_web("Pause sonore été.JPG"), "pause-sonore-ete.jpg")
    self.assertEqual(nom_web("  Mains   & Djembé (2).png"), "mains-djembe-2.png")
def test_preparer_ordre_et_url(self):  # f1 = src/Couverture.jpg, f2 = src/Diapo.jpg (petits JPEG créés avec Pillow)
    urls = preparer([f1, f2], "2026-11-10-idees-recues", racine=tmp)
    self.assertEqual(urls, [BASE_URL + "2026-11-10-idees-recues/01-couverture.jpg",
                            BASE_URL + "2026-11-10-idees-recues/02-diapo.jpg"])
    self.assertTrue((tmp / "medias-instagram/2026-11-10-idees-recues/01-couverture.jpg").exists())
def test_refus(self):
    with self.assertRaises(ValueError): preparer([f1], "Mauvais lot", racine=tmp)
    with self.assertRaises(ValueError): preparer([tmp / "son.m4a"], "2026-11-10-x", racine=tmp)
    with self.assertRaises(ValueError): preparer([gros_jpg_9_mo], "2026-11-10-x", racine=tmp)
def test_retirer(self):
    preparer([f1], "2026-11-10-x", racine=tmp); retirer("2026-11-10-x", racine=tmp)
    self.assertFalse((tmp / "medias-instagram/2026-11-10-x").exists())
def test_attendre_en_ligne(self): # Review Focus 4 — patch de medias.urllib.request.urlopen
    with patch("medias.urllib.request.urlopen", side_effect=[erreur_404(), erreur_404(), reponse_200()]):
        self.assertTrue(attendre_en_ligne([URL], delai_max=60, pas=0))
    with patch("medias.urllib.request.urlopen", side_effect=lambda *a, **k: (_ for _ in ()).throw(erreur_404())):
        self.assertFalse(attendre_en_ligne([URL], delai_max=0, pas=0))
```

- [ ] **Step 2 : Lancer, vérifier l'échec.**
- [ ] **Step 3 : Implémenter `medias.py`** (`nom_web` : nom et extension traités séparément ; `unicodedata` NFKD sans diacritiques, minuscules, tout ce qui n'est pas `[a-z0-9]` → `-`, tirets fusionnés puis retirés aux extrémités ; `urllib.request` pour `attendre_en_ligne`).
- [ ] **Step 4 : Modifier `robots.txt`.**
- [ ] **Step 5 : Relancer** → toute la suite passe.
- [ ] **Step 6 : Commit** — `feat(instagram): mise en ligne des médias (dossier caché du site)`

---

### Task 4 : Le skill et ses fichiers de référence

**Files :**
- Create : `.claude/skills/instagram-enza/SKILL.md`
- Create : `.claude/skills/instagram-enza/regles-contenu.md`, `themes.md`, `charte-visuelle.md`, `metricool.md`, `reponses-types.md`
- Create (hors dépôt) : `C:\Users\Sekai\Documents\Instagram-Enza\` avec `a-deposer\`, `posts\`, `references-style\`, `journal.md`
- Test : `.claude/skills/instagram-enza/tests/test_contenu_skill.py`

**Interfaces :**
- Consumes : CLI de `legende.py`, `visuel.rendre` / `rendre_carrousel`, `medias.preparer` / `attendre_en_ligne` / `retirer`.
- Produces : les déclencheurs « prépare la semaine », « Enza a validé », « bilan du mois », « réponse type », « bio » ; le format de `journal.md` : tableau `| date prévue | thème | sujet | format | statut | uuid Metricool | lot médias |`, statuts `proposé`, `brouillon`, `validé`, `programmé`, `publié`, `refusé`.

- [ ] **Step 1 : Écrire le test de contenu** : chaque phrase clé de la spec est bien quelque part dans le skill.

```python
ATTENDUS = {
  "SKILL.md": ["name: instagram-enza", "PRODUCT.md", "Enza a validé", "prépare la semaine", "bilan du mois",
               "Instagram-Enza", "en français"],
  "regles-contenu.md": ["ne remplace pas l'avis d'un médecin ou d'un spécialiste", "en formation",
                        "guérir", "0800 32 123", "107", "112", "accord écrit"],
  "themes.md": ["Comprendre", "Pour qui", "Ce que dit la recherche", "Une pause pour soi", "Coulisses"],
  "charte-visuelle.md": ["visage", "1080", "1350", "1920", "isAiGenerated", "libres de droits"],
  "metricool.md": ["getBrandSettings", "draft", "updateScheduledPost", "getBestTimeToPostByNetwork",
                   "mediaAltText", "attendre_en_ligne"],
  "reponses-types.md": ["utm_source=instagram", "utm_source=facebook", "0800 32 123"],
}
```
  Plus : le frontmatter de `SKILL.md` a `name` et `description` ; chaque fichier cité dans `SKILL.md` existe.

- [ ] **Step 2 : Lancer, vérifier l'échec.**
- [ ] **Step 3 : Écrire `SKILL.md`** (court, en français). Description avec déclencheurs : posts, carrousel, story, reel, Instagram, Facebook, Metricool, « prépare la semaine », « Enza a validé », « bilan du mois ». Corps : rôles ; les 5 déroulés de la spec (étapes 1 à 5) avec, pour chacun, quels fichiers lire et quels scripts lancer (étape 3 : si Metricool est indisponible pour Enza, l'utilisateur lui envoie l'image de chaque post ; étape 5 : l'utilisateur donne le nombre de demandes venues d'Instagram, lu dans Notion) ; règles d'or (les Global Constraints de sécurité : validation, visage, téléchargements, français) ; création du dossier de travail s'il manque.
- [ ] **Step 4 : Écrire les 5 fichiers de référence** à partir de la spec, sans recopier `PRODUCT.md` :
  - `regles-contenu.md` : promesses, intime, rappel, statut, personnes, recherche, détresse.
  - `themes.md` : les 5 thèmes avec leur part, une réserve de sujets par thème tirée des articles du site (`article-*.html`, `professionnels.html`), l'invitation à réserver (un post sur trois plus explicite).
  - `charte-visuelle.md` : style, formats, ce qui vient du vrai ou de l'IA, liste de contrôle qualité (mains, instruments, texte, aspect artificiel, couleurs criardes, cohérence, lisibilité sur téléphone), procédure du test de style, musique, sous-titres, texte alternatif.
  - `metricool.md` : `getBrandSettings` → `blogId` et fuseau ; création du brouillon (`createScheduledPost`, `providers` instagram + facebook, `draft: true`, `instagramData.type`, `facebookData.type`, `mediaAltText`, `isAiGenerated`) ; **avant** : `medias.preparer` → déploiement → `attendre_en_ligne` ; **après** : vérifier dans `getScheduledPosts` si Metricool a copié les médias (si oui, `medias.retirer`) ; validation : `getBestTimeToPostByNetwork` puis `updateScheduledPost` (`draft: false`) avec le contenu complet ; limites du plan gratuit ; `createScheduledPostForReview` indisponible.
  - `reponses-types.md` : tarifs, réservation, question médicale, demande de professionnel, personne en détresse ; textes de bio Instagram et Facebook avec rappel et lien UTM.
- [ ] **Step 5 : Créer le dossier de travail** et `journal.md` (en-tête du tableau + les 4 posts existants marqués `publié`).
- [ ] **Step 6 : Relancer** → toute la suite passe.
- [ ] **Step 7 : Commit** — `feat(instagram): skill instagram-enza (déroulé, règles, thèmes, charte, Metricool, réponses types)`

---

### Task 5 : Mise en service et répétition à blanc

**Files :** aucun nouveau (déploiement + essai).

- [ ] **Step 1 : Déployer** selon le flux habituel : fusion rapide de la branche du worktree dans `master`, push, puis vérifier en ligne que `https://musicotherapeute-hainaut.be/robots.txt` contient `Disallow: /medias-instagram/`.
- [ ] **Step 2 : Répétition à blanc de « prépare la semaine »**, sans aucune écriture dans Metricool : le skill se charge, lit le journal, propose 2 ou 3 sujets équilibrés entre thèmes, rédige une légende qui passe `legende.py` sans `BLOQUANT`, rend un carrousel sans débordement. Corriger le skill si une étape hésite ou contredit la spec.
- [ ] **Step 3 : Commit** des corrections éventuelles — `fix(instagram): ajustements après répétition à blanc`

---

### Task 6 : Premier lot (flyer corrigé + test de style)

**Files :**
- Create : `.claude/skills/instagram-enza/gabarits/flyer-tarifs.html`
- Modify : `.claude/skills/instagram-enza/gabarits/theme.css` (style retenu)
- Création dans le dossier de travail : `posts\<date>-flyer-tarifs\`, `references-style\`

- [ ] **Step 1 : Flyer corrigé** au format 1080 × 1350, dans l'esprit du flyer actuel (fond vert forêt, logo exact de `logo_Enza.svg`, rubriques « Séances et tarifs », « Selon vos besoins », « Infos et contact »), avec les tarifs et coordonnées des Global Constraints (atelier **1 h 30**). Rendu sans débordement, contrôle visuel.
- [ ] **Step 2 : Test de style** : une planche de 4 à 6 variantes de couverture (police de titre, vert, avec ou sans plante). Demander à l'utilisateur s'il active le connecteur de génération d'images pour ajouter des fonds IA ; sinon, test sans IA. Montrer la planche ; Enza choisit.
- [ ] **Step 3 : Reporter le choix** dans `theme.css` et copier les visuels retenus dans `references-style\`. Relancer la suite de tests.
- [ ] **Step 4 : Premier brouillon Metricool** (le flyer) en suivant `metricool.md` : préparer, déployer, attendre en ligne, `createScheduledPost` avec `draft: true`. **Vérifications d'intégration** : le brouillon apparaît dans `getScheduledPosts` ; noter si les médias ont été copiés par Metricool et l'inscrire dans `metricool.md`. Journal : `brouillon`.
- [ ] **Step 5 : Attendre « Enza a validé »**, puis programmer à la meilleure heure. Rappeler à l'utilisateur qu'Enza archive elle-même l'ancien flyer dans l'app (Metricool ne supprime pas un post publié). Journal : `programmé`.
- [ ] **Step 6 : Commit** — `feat(instagram): flyer des tarifs à jour et style de référence`

---

### Task 7 (conditionnelle) : Vidéos courtes

À lancer seulement quand Enza fournit un premier enregistrement **et** que l'utilisateur accepte d'installer `ffmpeg` (installation = accord explicite, par exemple `winget install Gyan.FFmpeg`).

**Files :**
- Create : `.claude/skills/instagram-enza/scripts/video.py`
- Test : `.claude/skills/instagram-enza/tests/test_video.py`

**Interfaces :**
- Produces : `assembler(visuels: list[Path], audio: Path | None, sous_titres: list[tuple[float, float, str]], sortie: Path, duree_par_visuel: float = 4.0) -> Path` : MP4 H.264 + AAC, 1080 × 1920, 30 i/s, ≤ 90 s, sous-titres incrustés en DM Sans.

- [ ] **Step 1 : Tests** : dimensions et durée lues avec `ffprobe` ; présence d'une piste audio quand `audio` est fourni ; `ValueError` au-delà de 90 s.
- [ ] **Step 2 : Lancer, vérifier l'échec.** **Step 3 : Implémenter.** **Step 4 : Relancer.**
- [ ] **Step 5 : Compléter `charte-visuelle.md` et `metricool.md`** (type `REEL`, couverture via `videoCoverMilliseconds`) ; ajuster `medias.py` si les vidéos dépassent 20 Mo (option : Google Drive relié à Metricool).
- [ ] **Step 6 : Commit** — `feat(instagram): assemblage des vidéos courtes`
