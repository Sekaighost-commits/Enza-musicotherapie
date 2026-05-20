# Plan d'implémentation — Section Témoignages

> **Pour les agents :** OBLIGATOIRE : utiliser superpowers:subagent-driven-development (si subagents disponibles) ou superpowers:executing-plans pour exécuter ce plan. Les étapes utilisent la syntaxe checkbox (`- [ ]`) pour le suivi.

**Spec de référence :** `docs/superpowers/specs/2026-05-20-section-temoignages-design.md`

**Goal :** Ajouter une section "Témoignages" sur `index.html` (entre Séances et Ressources), affichant initialement le témoignage de Virginie, avec une infrastructure HTML/CSS/JS prête à accueillir d'autres témoignages et un bouton "Lire d'autres témoignages" qui s'activera à partir de 4 entrées.

**Architecture :** Site statique HTML/CSS/JS sans build step. CSS et JS inline dans chaque fichier. Réutilisation des variables CSS existantes (`--cream`, `--slate`, `--green`, etc.). Le JS toggle est ajouté dans le bloc `<script>` existant en bas de `index.html`. Pas de framework, pas de dépendance ajoutée.

**Tech Stack :** HTML5, CSS3 (variables existantes), JavaScript vanilla. Pas de tests automatisés (site statique sans test runner) — la validation se fait visuellement dans le navigateur.

---

## File Structure

| Fichier | Action | Responsabilité |
|---|---|---|
| `index.html` | Modifier | Ajouter la section `#temoignages`, son CSS inline, et le JS de toggle (dormant tant que < 4 témoignages) |
| `mentions-legales.html` | Modifier | Ajouter une sous-section `<h3>Témoignages</h3>` dans `#donnees` |

Total : 2 fichiers modifiés. Aucun nouveau fichier.

---

## Chunk 1: Section HTML et CSS sur index.html

### Task 1 : Ajouter les règles CSS pour la nouvelle section

**Files:**
- Modifier : `index.html` (bloc `<style>` dans le `<head>`, après les autres règles de section)

- [ ] **Étape 1 : Localiser la fin du bloc `<style>` dans `index.html`**

Lire `index.html` autour des lignes 1100-1200 pour trouver un bon endroit d'insertion (après les autres règles `.sec-*` et avant la fermeture `</style>`). Repérer la ligne exacte.

- [ ] **Étape 2 : Insérer les règles CSS de la section témoignages**

Insérer ce bloc CSS avant la balise `</style>` :

```css
/* ── TÉMOIGNAGES ── */
.sec-temoignages {
  background: var(--cream);
  padding: 7rem 2rem;
}
.temoignages-header {
  text-align: center;
  max-width: 720px;
  margin: 0 auto 3.5rem;
}
.temoignages-header .section-tag--bordered {
  display: inline-block;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--green);
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--green);
  margin-bottom: 1.5rem;
  font-weight: 500;
}
.temoignages-header h2 {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 2rem;
  color: var(--slate);
  margin: 0 0 1rem;
  line-height: 1.2;
}
.temoignages-consent {
  font-family: 'DM Sans', sans-serif;
  font-style: italic;
  font-size: 0.85rem;
  color: var(--slate-mid);
  margin: 0;
}
.temoignages-list {
  max-width: 720px;
  margin: 0 auto;
  padding: 0 1rem;
}
.temoignage {
  padding: 2rem 0;
}
.temoignage + .temoignage {
  border-top: 1px solid rgba(122,158,126,0.25);
}
.temoignage-quote {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 1.15rem;
  color: var(--slate);
  line-height: 1.7;
  margin: 0 0 1rem;
}
.temoignage-quote:last-of-type {
  margin-bottom: 1.25rem;
}
.temoignage-author {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--slate-mid);
  font-weight: 400;
  margin: 0;
}
/* Bouton "Lire d'autres témoignages" — dormant tant que < 4 témoignages */
.temoignages-toggle {
  display: none; /* Activé par JS quand il y a des témoignages masqués */
  margin: 2.5rem auto 0;
  background: transparent;
  border: 1px solid var(--green);
  color: var(--green-dark);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.85rem 1.6rem;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}
.temoignages-toggle:hover,
.temoignages-toggle:focus-visible {
  background: var(--green);
  color: var(--cream);
}
.temoignages-toggle.visible {
  display: block;
}
/* Témoignages masqués — transition douce (la spec impose max-height + opacity, non animables sur display:none) */
.temoignage.is-hidden {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  border-top: 0 !important;
  overflow: hidden;
  transition: max-height 0.6s ease, opacity 0.4s ease, padding 0.4s ease;
}
.temoignage {
  max-height: 200rem;
  opacity: 1;
  overflow: hidden;
  transition: max-height 0.6s ease, opacity 0.4s ease, padding 0.4s ease;
}
@media (max-width: 768px) {
  .sec-temoignages { padding: 5rem 1.5rem; }
  .temoignages-header h2 { font-size: 1.6rem; }
  .temoignage-quote { font-size: 1.05rem; }
}
```

- [ ] **Étape 3 : Commit intermédiaire**

```bash
git add index.html
git commit -m "style(temoignages): ajoute les règles CSS pour la section témoignages"
```

---

### Task 2 : Ajouter le HTML de la section sur `index.html`

**Files:**
- Modifier : `index.html` (entre `</section>` de `#seances` et `<section id="ressources">`)

- [ ] **Étape 1 : Localiser la fermeture de la section `#seances`**

Lire `index.html` autour des lignes 1384-1470 pour trouver le `</section>` qui ferme `#seances` (vers la ligne 1470) et le `<section id="ressources">` qui commence juste après.

- [ ] **Étape 2 : Insérer le HTML de la section**

Insérer ce bloc HTML entre la fermeture de `#seances` et le début de `#ressources` :

```html

  <!-- TÉMOIGNAGES -->
  <section id="temoignages" class="sec-temoignages">
    <div class="temoignages-header fade-up">
      <span class="section-tag--bordered">Témoignages</span>
      <h2>Ce qu'en disent les personnes accompagnées</h2>
      <p class="temoignages-consent">Témoignages partagés avec l'accord des personnes concernées. Prénoms modifiés à la demande.</p>
    </div>

    <div class="temoignages-list" id="temoignages-list">

      <article class="temoignage fade-up">
        <p class="temoignage-quote">« J'ai accompagné ma maman, atteinte de la maladie d'Alzheimer sévère, pour une séance de musicothérapie avec Enza, et l'expérience a été très positive. Enza fait preuve d'une grande bienveillance, de douceur et d'une écoute attentive, ce qui met rapidement en confiance. Elle a su créer un cadre apaisant et adapté, dans lequel ma maman s'est sentie à l'aise et réceptive.</p>
        <p class="temoignage-quote">La séance s'est déroulée dans une atmosphère sereine et respectueuse du rythme de chacun. On sent une réelle envie d'aider et d'accompagner avec le cœur, ce qui est précieux dans ce type d'accompagnement.</p>
        <p class="temoignage-quote">Même si elle est encore en début de parcours, son approche est déjà très prometteuse. Je recommande Enza pour sa gentillesse, son implication et la qualité de sa présence. »</p>
        <p class="temoignage-author">Virginie · Intervention en Institut</p>
      </article>

      <!-- Ajouter d'autres <article class="temoignage fade-up"> ici.
           Au-delà de 3 témoignages, ajouter la classe "is-hidden" sur ceux à masquer par défaut. -->

    </div>

    <button type="button"
            class="temoignages-toggle"
            id="temoignages-toggle"
            aria-expanded="false"
            aria-controls="temoignages-list">
      Lire d'autres témoignages
    </button>
  </section>
```

- [ ] **Étape 3 : Vérifier le rendu visuel dans le navigateur**

Ouvrir `index.html` dans le navigateur (localement, double-clic ou via le panneau de prévisualisation). Scroller jusqu'à la nouvelle section. Vérifier :
- Elle apparaît bien entre Séances et Ressources
- Le tag "Témoignages" a une bordure verte
- Le titre est en italique Cormorant Garamond
- La note de consentement est en italique gris discret
- Le témoignage de Virginie est lisible, guillemets bien placés (au début du 1er paragraphe et à la fin du 3e)
- L'attribution est en uppercase lettrespaced
- Pas de bouton "Lire d'autres témoignages" visible (un seul témoignage, JS pas encore actif)

- [ ] **Étape 4 : Vérifier le rendu mobile (DevTools responsive, 375px)**

- Padding réduit correct
- Titre h2 plus petit (1.6rem)
- Citation lisible (1.05rem)
- Pas de débordement horizontal

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat(temoignages): ajoute la section témoignages avec le premier témoignage (Virginie)"
```

---

### Task 3 : Ajouter le JS de toggle (dormant)

**Files:**
- Modifier : `index.html` (bloc `<script>` à la fin du `<body>`)

- [ ] **Étape 1 : Localiser le bloc `<script>` existant**

Lire `index.html` autour des lignes 1665-1700 pour trouver le bloc `<script>` existant qui contient déjà le `nav scroll`, le `IntersectionObserver`, le `FAQ accordion`, et le `contact form submit`.

- [ ] **Étape 2 : Insérer la logique de toggle juste avant la fin du `<script>`**

Insérer ce bloc JS dans le `<script>`, avant l'écouteur `contact-form` (ou à un emplacement cohérent avec les autres fonctionnalités) :

```javascript
    // ── TÉMOIGNAGES — Bouton "Lire d'autres témoignages" ──
    (function() {
      const list = document.getElementById('temoignages-list');
      const toggle = document.getElementById('temoignages-toggle');
      if (!list || !toggle) return;

      const hiddenItems = list.querySelectorAll('.temoignage.is-hidden');
      if (hiddenItems.length === 0) return; // Aucun témoignage masqué → bouton reste caché

      // Active l'affichage du bouton et personnalise le libellé
      toggle.classList.add('visible');
      toggle.textContent = `Lire d'autres témoignages (${hiddenItems.length})`;

      let expanded = false;
      toggle.addEventListener('click', () => {
        expanded = !expanded;
        hiddenItems.forEach(el => el.classList.toggle('is-hidden', !expanded));
        toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        toggle.textContent = expanded
          ? 'Replier les témoignages'
          : `Lire d'autres témoignages (${hiddenItems.length})`;
      });
    })();
```

- [ ] **Étape 3 : Vérifier que le JS n'a pas cassé la page**

Recharger `index.html` dans le navigateur. Ouvrir la console (F12) : aucune erreur JS attendue. Le bouton "Lire d'autres témoignages" doit toujours être absent visuellement (puisqu'aucun témoignage n'a la classe `is-hidden`).

- [ ] **Étape 4 : Test manuel de la logique d'expansion (futur)**

Pour vérifier que le JS marchera bien quand on ajoutera des témoignages, **temporairement** ajouter dans `index.html` 4 témoignages factices (3 visibles + 1 avec `class="temoignage is-hidden"`). Sauvegarder, recharger. Vérifier :
- Le bouton apparaît avec le libellé "Lire d'autres témoignages (1)"
- Au clic, le 4e témoignage apparaît
- Le bouton devient "Replier les témoignages"
- Re-clic : le 4e disparaît, le bouton redevient "Lire d'autres témoignages (1)"
- L'attribut `aria-expanded` change correctement (inspecter le DOM)

Puis **retirer les 3 témoignages factices** (revenir à l'état avec uniquement Virginie). Ne pas committer les témoignages factices.

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat(temoignages): ajoute le JS de toggle pour le bouton 'Lire d'autres témoignages'"
```

---

## Chunk 2: Mentions légales

### Task 4 : Ajouter la sous-section RGPD pour les témoignages

**Files:**
- Modifier : `mentions-legales.html` (section `#donnees`)

- [ ] **Étape 1 : Localiser la section `#donnees`**

Lire `mentions-legales.html` autour des lignes 240-290 pour trouver la section `<section class="legal-section" id="donnees">` et identifier où insérer la nouvelle sous-section. Elle doit aller **avant** la sous-section "Sous-traitants" (`<h3>Sous-traitants</h3>`) pour rester dans une logique de "qu'est-ce qu'on traite, puis avec qui".

- [ ] **Étape 2 : Insérer la sous-section témoignages**

Insérer ce bloc HTML juste avant `<h3>Sous-traitants</h3>` :

```html
      <h3>Témoignages</h3>
      <p>Certaines pages du site (notamment la page d'accueil) affichent des témoignages de personnes accompagnées. Ces témoignages sont publiés selon les modalités suivantes :</p>
      <ul>
        <li><strong>Consentement explicite</strong> : aucun témoignage n'est publié sans l'accord écrit (par email) de la personne concernée.</li>
        <li><strong>Anonymisation</strong> : seul le prénom est affiché, suivi du contexte général de l'accompagnement (ex. : "Suivi individuel", "Intervention en institut"). Aucun nom de famille, aucune information de santé spécifique permettant l'identification d'une personne tierce (ex. : un proche accompagné).</li>
        <li><strong>Droit de retrait</strong> : toute personne ayant donné son témoignage peut demander à tout moment son retrait par simple email à <a href="mailto:enza@musicotherapeute-hainaut.be">enza@musicotherapeute-hainaut.be</a>. Le retrait sera effectif dans les meilleurs délais, sans justification à fournir.</li>
        <li><strong>Durée de conservation</strong> : les témoignages sont conservés tant qu'ils sont pertinents pour la communication du site, et retirés sans délai sur demande de la personne concernée.</li>
      </ul>
```

- [ ] **Étape 3 : Vérifier visuellement**

Ouvrir `mentions-legales.html` dans le navigateur, naviguer jusqu'à la section "Données personnelles". Vérifier :
- La sous-section "Témoignages" apparaît avant "Sous-traitants"
- Les puces sont bien formatées
- Le lien email est cliquable
- Le style suit celui des autres sous-sections

- [ ] **Étape 4 : Commit**

```bash
git add mentions-legales.html
git commit -m "docs(legal): ajoute la sous-section RGPD sur les témoignages"
```

---

## Chunk 3: Validation finale et déploiement

### Task 5 : Validation visuelle complète

- [ ] **Étape 1 : Tester `index.html` sur Chrome desktop**

Ouvrir `index.html` dans Chrome. Faire dérouler la page de haut en bas. Vérifier :
- La nouvelle section apparaît au bon endroit (entre Séances et Ressources)
- L'animation `fade-up` se déclenche au scroll (le contenu apparaît avec un léger délai et un translate)
- Pas de débordement, pas d'erreur console
- Les autres sections n'ont pas été affectées (Séances, Ressources, FAQ, Contact toujours OK)

- [ ] **Étape 2 : Tester `index.html` sur DevTools mobile (375px width)**

Ouvrir DevTools (F12) → mode responsive → 375px (iPhone SE). Vérifier :
- Le padding de la section est réduit (5rem au lieu de 7rem)
- Le titre h2 est en 1.6rem (lisible mais pas géant)
- Les citations sont en 1.05rem
- Pas de débordement horizontal (scroll horizontal interdit)

- [ ] **Étape 3 : Tester `mentions-legales.html`**

Ouvrir `mentions-legales.html`. Vérifier que la section "Données personnelles" contient bien la nouvelle sous-section "Témoignages" avant "Sous-traitants". Vérifier que le lien email fonctionne.

- [ ] **Étape 4 : Audit console (Chrome DevTools → Console + Lighthouse)**

- Aucune erreur ni warning JS sur les deux pages
- Lighthouse Accessibility ≥ 95 (test rapide, non bloquant)

---

### Task 6 : Merger sur master et pousser en production

- [ ] **Étape 1 : Vérifier l'état git**

```bash
git status
git log --oneline -5
```

Attendu : tous les commits du plan sont présents sur la branche `claude/eloquent-kalam-ae686c`, working tree clean.

- [ ] **Étape 2 : Merger sur master**

Exécuter depuis le worktree principal (pas le worktree feature) :

```bash
MASTER_WT="C:/Users/Sekai/Claude Projets/Enza-musicothérapie"
git -C "$MASTER_WT" merge --ff-only claude/eloquent-kalam-ae686c
```

Attendu : `Fast-forward` réussi, master pointe sur le dernier commit du plan.

- [ ] **Étape 3 : Pousser sur GitHub**

```bash
git -C "$MASTER_WT" push origin master
```

Attendu : push réussi. GitHub Pages redéploie automatiquement.

- [ ] **Étape 4 : Vérifier en production (après 1-2 min)**

Ouvrir https://musicotherapeute-hainaut.be → scroller jusqu'à la section Témoignages → vérifier le rendu final. Vérifier aussi `https://musicotherapeute-hainaut.be/mentions-legales.html` → section "Données personnelles" → sous-section "Témoignages" présente.

---

## Notes pour l'implémenteur

- **Ne pas committer de témoignages factices** créés pour tester le toggle JS (Task 3, étape 4). Les retirer avant le commit final.
- **Pas de tests automatisés** : ce projet est statique, pas de framework de test. Toute la validation est visuelle.
- **Si une étape échoue** : ne pas continuer. Diagnostiquer (console, inspecter le DOM, comparer avec la spec) avant de passer à la suite.
- **Cohérence des classes CSS** : les classes utilisées (`.sec-temoignages`, `.temoignage`, `.temoignages-toggle`, etc.) sont nouvelles et ne risquent pas de collision avec l'existant. Vérifier néanmoins avec `grep` rapide si un doute survient.
- **Le bouton "Lire d'autres témoignages" est dormant** : pas visible tant qu'aucun témoignage n'a la classe `is-hidden`. C'est volontaire — la spec impose une infrastructure prête pour le futur, sans bouton visible à 1 témoignage.
