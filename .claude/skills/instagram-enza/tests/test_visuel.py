"""Tests du rendu des visuels (scripts/visuel.py)."""
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

RACINE_SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE_SKILL / "scripts"))

from visuel import DebordementTexte, PoliceManquante, TexteInterdit, rendre, rendre_carrousel  # noqa: E402

G = RACINE_SKILL / "gabarits"


class TestVisuel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._dossier = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._dossier.name)

    @classmethod
    def tearDownClass(cls):
        cls._dossier.cleanup()

    def test_taille_et_format(self):
        p = rendre(G / "couverture.html", {"titre": "Pour qui ?"}, self.tmp / "a.jpg")
        with Image.open(p) as im:
            self.assertEqual((im.size, im.format, im.mode), ((1080, 1350), "JPEG", "RGB"))

    def test_extension_jpg_imposee(self):
        p = rendre(G / "diapo.html", {"titre": "Titre", "texte": "Texte"}, self.tmp / "e.png")
        self.assertEqual(p.suffix, ".jpg")
        self.assertTrue(p.exists())

    def test_story(self):
        p = rendre(G / "story.html", {"titre": "Atelier samedi"}, self.tmp / "s.jpg", format="story")
        with Image.open(p) as im:
            self.assertEqual(im.size, (1080, 1920))

    def test_texte_trop_long(self):  # Review Focus 2
        with self.assertRaises(DebordementTexte):
            rendre(G / "couverture.html", {"titre": "Musicothérapie " * 40}, self.tmp / "b.jpg")

    def test_echappement_html(self):
        p = rendre(G / "diapo.html", {"titre": "<b>« À deux »</b>", "texte": "Écoute & souffle"},
                   self.tmp / "c.jpg")
        self.assertTrue(p.exists())

    def test_carrousel(self):
        ps = rendre_carrousel([(G / "couverture.html", {"titre": "1"}), (G / "fin.html", {"titre": "2"})],
                              self.tmp / "carrousel")
        self.assertEqual([p.name for p in ps], ["01.jpg", "02.jpg"])
        with self.assertRaises(ValueError):
            rendre_carrousel([(G / "diapo.html", {})] * 11, self.tmp / "trop")

    def test_image_de_fond_visible(self):  # relecture finale, Important 1
        rouge = self.tmp / "rouge.png"
        Image.new("RGB", (100, 100), (255, 0, 0)).save(rouge)
        p = rendre(G / "couverture.html", {"titre": "Test", "fond": str(rouge)}, self.tmp / "fond.jpg")
        with Image.open(p) as im:
            r, g, b = im.getpixel((540, 20))
        self.assertGreater(r, 200)
        self.assertLess(g, 60)

    def test_promesse_refusee_dans_un_visuel(self):  # relecture finale, Important 2
        with self.assertRaises(TexteInterdit):
            rendre(G / "diapo.html", {"titre": "Bienfaits", "texte": "La musique peut guérir l'anxiété."},
                   self.tmp / "promesse.jpg")

    def test_police_manquante(self):
        g = self.tmp / "police-inexistante.html"
        g.write_text('<!doctype html><html><head><meta charset="utf-8">'
                     '<style>:root{--polices:"Police Inexistante"}</style></head>'
                     '<body><div data-cadre style="font-family:\'Police Inexistante\'">$titre</div></body></html>',
                     encoding="utf-8")
        with self.assertRaises(PoliceManquante):
            rendre(g, {"titre": "Test"}, self.tmp / "d.jpg")


if __name__ == "__main__":
    unittest.main()
