"""Rendu des visuels Instagram d'Enza : gabarit HTML + champs -> JPEG aux dimensions exactes.

    from visuel import rendre, rendre_carrousel
    rendre(GABARITS / "couverture.html", {"titre": "Pour qui ?"}, Path("couverture.jpg"))

Champs : titre, sous_titre, texte, pied (adresse du site par défaut), fond (chemin d'une image).
Le rendu s'arrête avec DebordementTexte si un texte sort de son cadre ou de l'image,
et avec PoliceManquante si une police du thème n'a pas pu être chargée.
"""
import html
import string
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

FORMATS = {"post": (1080, 1350), "story": (1080, 1920)}
MAX_DIAPOS = 10
GABARITS = Path(__file__).resolve().parents[1] / "gabarits"
DEFAUTS = {"pied": "musicotherapeute-hainaut.be"}

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


def _remplir(gabarit: Path, champs: dict) -> str:
    modele = string.Template(gabarit.read_text(encoding="utf-8"))
    valeurs = {k: "" for k in modele.get_identifiers()}
    valeurs.update({k: v for k, v in DEFAUTS.items() if k in valeurs})
    for cle, valeur in champs.items():
        if cle != "fond":
            valeurs[cle] = html.escape(str(valeur), quote=True)
    fond = champs.get("fond")
    if fond:
        chemin = Path(fond).resolve(strict=True)
        valeurs["fond_css"] = f'url("{chemin.as_uri()}")'
    else:
        valeurs["fond_css"] = "none"
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
    dossier = Path(dossier)
    with sync_playwright() as p:
        b = p.chromium.launch()
        try:
            page = b.new_page(viewport={"width": largeur, "height": hauteur}, device_scale_factor=1)
            return [_rendre_page(page, g, champs, dossier / f"{i:02d}.jpg")
                    for i, (g, champs) in enumerate(diapos, start=1)]
        finally:
            b.close()
