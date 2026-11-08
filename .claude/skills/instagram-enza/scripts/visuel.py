"""Rendu des visuels Instagram d'Enza : gabarit HTML + champs -> JPEG aux dimensions exactes.

    from visuel import rendre, rendre_carrousel
    rendre(GABARITS / "couverture.html", {"titre": "Pour qui ?"}, Path("couverture.jpg"))

Champs : titre, sous_titre, texte, pied (adresse du site par défaut), fond (chemin d'une image ;
sans lui, le fond par défaut du thème, --fond-image dans theme.css), variante (aquarelle, creme,
tendre, foret), photo (chemin, pour photo.html et arche.html), cadrage (position de la photo, « 50% 30% »).
Chaque gabarit a ses propres champs : voir le tableau des visages dans charte-visuelle.md.
Le rendu s'arrête avec DebordementTexte si un texte sort de son cadre ou de l'image,
et avec PoliceManquante si une police du thème n'a pas pu être chargée.
"""
import html
import string
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from legende import verifier  # noqa: E402

FORMATS = {"post": (1080, 1350), "story": (1080, 1920)}
MAX_DIAPOS = 10
GABARITS = Path(__file__).resolve().parents[1] / "gabarits"
DEFAUTS = {"pied": "musicotherapeute-hainaut.be", "cadrage": "50% 50%"}
# Champs qui ne sont pas du texte affiché : jamais passés au contrôle des promesses.
CHAMPS_TECHNIQUES = {"fond", "photo", "cadrage", "variante"}
# Couleur de fond d'une couverture, d'une diapo ou d'une story (vide = aquarelle par défaut).
VARIANTES = {"", "aquarelle", "creme", "tendre", "foret"}

_CONTROLE_JS = """
async () => {
  await document.fonts.ready;
  const liste = getComputedStyle(document.documentElement).getPropertyValue('--polices');
  const familles = liste.split(',').map(s => s.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
  const manquantes = [];
  for (const f of familles) {
    const faces = await document.fonts.load(`16px "${f}"`);
    if (!faces.length) manquantes.push(f);
  }
  await document.fonts.ready;
  // Zone de sécurité = boîte de contenu de .page (l'image moins ses marges intérieures).
  // On ne compare pas scrollHeight/clientHeight : les lettres d'une grande police dépassent
  // toujours un peu de l'interligne sans que le texte soit coupé.
  const debord = [];
  for (const el of document.querySelectorAll('[data-cadre]')) {
    if (!el.textContent.trim() || getComputedStyle(el).display === 'none') continue;
    const cadre = el.closest('.page') || document.body;
    const c = cadre.getBoundingClientRect(), s = getComputedStyle(cadre);
    const zone = {
      left: c.left + parseFloat(s.paddingLeft), right: c.right - parseFloat(s.paddingRight),
      top: c.top + parseFloat(s.paddingTop), bottom: c.bottom - parseFloat(s.paddingBottom),
    };
    const r = el.getBoundingClientRect();
    if (el.scrollWidth > el.clientWidth + 1 ||
        r.left < zone.left - 1 || r.right > zone.right + 1 ||
        r.top < zone.top - 1 || r.bottom > zone.bottom + 1) {
      debord.push(el.textContent.trim().slice(0, 40));
    }
  }
  return {manquantes, debord};
}
"""


class DebordementTexte(Exception):
    """Un texte sort de son cadre ou de l'image : le raccourcir."""


class PoliceManquante(Exception):
    """Une police du thème n'a pas été chargée (connexion ? nom de police ?)."""


class TexteInterdit(Exception):
    """Le texte d'un visuel contient une promesse de guérison (mêmes règles que legende.py)."""


def _controler_textes(champs: dict) -> None:
    texte = " ".join(str(v) for cle, v in champs.items() if cle not in CHAMPS_TECHNIQUES)
    for r in verifier(texte):
        if r.regle == "promesse":
            raise TexteInterdit(r.message)


def _remplir(gabarit: Path, champs: dict) -> str:
    modele = string.Template(gabarit.read_text(encoding="utf-8"))
    valeurs = {k: "" for k in modele.get_identifiers()}
    valeurs.update({k: v for k, v in DEFAUTS.items() if k in valeurs})
    for cle, valeur in champs.items():
        if cle not in ("fond", "photo"):
            valeurs[cle] = html.escape(str(valeur), quote=True)
    variante = str(champs.get("variante", ""))
    if variante not in VARIANTES:
        raise ValueError(f"Variante inconnue : {variante!r} (possibles : {', '.join(sorted(VARIANTES - {''}))})")
    if "photo" in valeurs:
        if not champs.get("photo"):
            raise ValueError(f"Le gabarit {gabarit.name} demande une photo (champ « photo »).")
        valeurs["photo"] = html.escape(Path(champs["photo"]).resolve(strict=True).as_uri(), quote=True)
    fond = champs.get("fond")
    if fond:
        chemin = Path(fond).resolve(strict=True)
        # Apostrophes : la valeur va dans un attribut style="…" entre guillemets doubles.
        valeurs["fond_css"] = f"url('{chemin.as_uri()}')"
    else:
        # Sans image fournie : le fond par défaut du thème (--fond-image dans theme.css), sinon rien.
        valeurs["fond_css"] = "var(--fond-image, none)"
    valeurs["base"] = gabarit.resolve().parent.as_uri() + "/"
    return modele.safe_substitute(valeurs)


def _rendre_page(page, gabarit: Path, champs: dict, sortie: Path) -> Path:
    sortie = Path(sortie).with_suffix(".jpg")
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        fichier = Path(d) / "rendu.html"
        fichier.write_text(_remplir(Path(gabarit), champs), encoding="utf-8")
        page.goto(fichier.as_uri(), wait_until="networkidle")
        etat = page.evaluate(_CONTROLE_JS)
    if etat["manquantes"]:
        raise PoliceManquante(f"Police(s) non chargée(s) : {', '.join(etat['manquantes'])}")
    if etat["debord"]:
        raise DebordementTexte("Texte trop long, à raccourcir : " + " | ".join(etat["debord"]))
    page.screenshot(path=str(sortie), type="jpeg", quality=90)
    return sortie


def _navigateur(format: str):
    if format not in FORMATS:
        raise ValueError(f"Format inconnu : {format!r} (attendu : {', '.join(FORMATS)})")
    return FORMATS[format]


def rendre(gabarit: Path, champs: dict[str, str], sortie: Path, format: str = "post") -> Path:
    largeur, hauteur = _navigateur(format)
    _controler_textes(champs)
    with sync_playwright() as p:
        b = p.chromium.launch()
        try:
            page = b.new_page(viewport={"width": largeur, "height": hauteur}, device_scale_factor=1)
            return _rendre_page(page, gabarit, champs, sortie)
        finally:
            b.close()


def rendre_carrousel(diapos: list[tuple[Path, dict[str, str]]], dossier: Path, format: str = "post") -> list[Path]:
    if len(diapos) > MAX_DIAPOS:
        raise ValueError(f"{len(diapos)} diapos : {MAX_DIAPOS} maximum par carrousel.")
    largeur, hauteur = _navigateur(format)
    for _, champs in diapos:
        _controler_textes(champs)
    dossier = Path(dossier)
    with sync_playwright() as p:
        b = p.chromium.launch()
        try:
            page = b.new_page(viewport={"width": largeur, "height": hauteur}, device_scale_factor=1)
            return [_rendre_page(page, g, champs, dossier / f"{i:02d}.jpg")
                    for i, (g, champs) in enumerate(diapos, start=1)]
        finally:
            b.close()
