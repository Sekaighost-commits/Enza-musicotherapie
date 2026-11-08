"""Tests de la mise en ligne des médias (scripts/medias.py)."""
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from medias import BASE_URL, attendre_en_ligne, nom_web, preparer, retirer  # noqa: E402

URL = BASE_URL + "2026-11-10-x/01-couverture.jpg"


def erreur_404():
    return urllib.error.HTTPError(URL, 404, "Not Found", hdrs=None, fp=None)


def reponse_200():
    r = MagicMock()
    r.status = 200
    r.__enter__.return_value = r
    return r


class TestMedias(unittest.TestCase):
    def setUp(self):
        self._dossier = tempfile.TemporaryDirectory()
        self.tmp = Path(self._dossier.name)
        src = self.tmp / "src"
        src.mkdir()
        self.f1, self.f2 = src / "Couverture.jpg", src / "Diapo.jpg"
        for f in (self.f1, self.f2):
            Image.new("RGB", (20, 25), "white").save(f, "JPEG")

    def tearDown(self):
        self._dossier.cleanup()

    def test_nom_web(self):  # Review Focus 3
        self.assertEqual(nom_web("Pause sonore été.JPG"), "pause-sonore-ete.jpg")
        self.assertEqual(nom_web("  Mains   & Djembé (2).png"), "mains-djembe-2.png")

    def test_preparer_ordre_et_url(self):
        urls = preparer([self.f1, self.f2], "2026-11-10-idees-recues", racine=self.tmp)
        self.assertEqual(urls, [BASE_URL + "2026-11-10-idees-recues/01-couverture.jpg",
                                BASE_URL + "2026-11-10-idees-recues/02-diapo.jpg"])
        self.assertTrue((self.tmp / "medias-instagram/2026-11-10-idees-recues/01-couverture.jpg").exists())

    def test_refus(self):
        with self.assertRaises(ValueError):
            preparer([self.f1], "Mauvais lot", racine=self.tmp)
        son = self.tmp / "son.m4a"
        son.write_bytes(b"\0" * 10)
        with self.assertRaises(ValueError):
            preparer([son], "2026-11-10-x", racine=self.tmp)
        gros = self.tmp / "gros.jpg"
        gros.write_bytes(b"\0" * (9 * 1024 * 1024))
        with self.assertRaises(ValueError):
            preparer([gros], "2026-11-10-x", racine=self.tmp)

    def test_retirer(self):
        preparer([self.f1], "2026-11-10-x", racine=self.tmp)
        retirer("2026-11-10-x", racine=self.tmp)
        self.assertFalse((self.tmp / "medias-instagram/2026-11-10-x").exists())

    def test_attendre_en_ligne(self):  # Review Focus 4
        with patch("medias.urllib.request.urlopen", side_effect=[erreur_404(), erreur_404(), reponse_200()]):
            self.assertTrue(attendre_en_ligne([URL], delai_max=60, pas=0))
        with patch("medias.urllib.request.urlopen", side_effect=lambda *a, **k: (_ for _ in ()).throw(erreur_404())):
            self.assertFalse(attendre_en_ligne([URL], delai_max=0, pas=0))


if __name__ == "__main__":
    unittest.main()
