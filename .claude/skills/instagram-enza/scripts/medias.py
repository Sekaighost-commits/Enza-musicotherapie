"""Mise en ligne des médias des posts dans un dossier caché du site.

Metricool exige des URL publiques. Les visuels sont copiés dans
<site>/medias-instagram/<lot>/ (exclu des moteurs par robots.txt), puis le site
est déployé avec le flux habituel (commit, fusion dans master, push).
Avant d'envoyer les URL à Metricool : attendre_en_ligne(urls).
Quand les médias ne servent plus : retirer(lot), puis redéployer.
"""
import re
import shutil
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

RACINE_SITE = Path(__file__).resolve().parents[4]
BASE_URL = "https://musicotherapeute-hainaut.be/medias-instagram/"
DOSSIER = "medias-instagram"
LOT = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
IMAGES = {".jpg", ".jpeg", ".png"}
VIDEOS = {".mp4"}
MAX_IMAGE = 8 * 1024 * 1024    # limite d'Instagram pour une image
MAX_VIDEO = 20 * 1024 * 1024   # au-delà, ne pas passer par le dépôt du site


def _slug(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def nom_web(nom: str) -> str:
    p = Path(nom.strip())
    return f"{_slug(p.stem)}{p.suffix.lower()}"


def _verifier_lot(lot: str) -> None:
    if not LOT.match(lot):
        raise ValueError(f"Nom de lot invalide : {lot!r} (attendu : AAAA-MM-JJ-sujet-en-minuscules).")


def preparer(fichiers: list[Path], lot: str, racine: Path = RACINE_SITE) -> list[str]:
    _verifier_lot(lot)
    for f in map(Path, fichiers):
        ext = f.suffix.lower()
        if ext not in IMAGES | VIDEOS:
            raise ValueError(f"{f.name} : format non accepté (jpg, png ou mp4 seulement).")
        limite = MAX_IMAGE if ext in IMAGES else MAX_VIDEO
        if f.stat().st_size > limite:
            raise ValueError(f"{f.name} : {f.stat().st_size / 1048576:.1f} Mo, maximum {limite // 1048576} Mo.")
    dest = Path(racine) / DOSSIER / lot
    dest.mkdir(parents=True, exist_ok=True)
    urls = []
    for i, f in enumerate(map(Path, fichiers), start=1):
        nom = f"{i:02d}-{nom_web(f.name)}"
        shutil.copy2(f, dest / nom)
        urls.append(f"{BASE_URL}{lot}/{nom}")
    return urls


def retirer(lot: str, racine: Path = RACINE_SITE) -> None:
    _verifier_lot(lot)
    shutil.rmtree(Path(racine) / DOSSIER / lot, ignore_errors=True)


def _en_ligne(url: str) -> bool:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="GET"), timeout=10) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        e.close()
        return False
    except (urllib.error.URLError, OSError):
        return False


def attendre_en_ligne(urls: list[str], delai_max: int = 300, pas: int = 15) -> bool:
    restantes = list(urls)
    debut = time.monotonic()
    while True:
        restantes = [u for u in restantes if not _en_ligne(u)]
        if not restantes:
            return True
        if time.monotonic() - debut >= delai_max:
            return False
        time.sleep(pas)
