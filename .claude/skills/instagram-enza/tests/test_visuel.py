"""Tests du rendu des visuels (scripts/visuel.py)."""
import re
import shutil
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

    def test_fond_par_defaut_du_theme(self):  # style B4 : le thème fournit le fond quand le post n'en donne pas
        g2 = self.tmp / "gabarits-fond-defaut"
        shutil.copytree(G, g2)
        Image.new("RGB", (100, 100), (0, 0, 255)).save(g2 / "bleu.png")
        with open(g2 / "theme.css", "a", encoding="utf-8") as f:
            f.write('\n:root { --fond-image: url("bleu.png"); }\n')
        p = rendre(g2 / "couverture.html", {"titre": "Test"}, self.tmp / "fond-defaut.jpg")
        with Image.open(p) as im:
            r, g, b = im.getpixel((540, 20))
        self.assertGreater(b, 200)
        self.assertLess(r, 60)

    def test_fond_du_theme_present(self):
        css = (G / "theme.css").read_text(encoding="utf-8")
        m = re.search(r'--fond-image:\s*url\("([^"]+)"\)', css)
        self.assertIsNotNone(m, "theme.css doit définir --fond-image")
        for chemin in re.findall(r'url\("(fonds/[^"]+)"\)', css):  # tous les fonds du thème
            self.assertTrue((G / chemin).is_file(), f"fichier introuvable : {chemin}")

    # --- Les 8 visages (variété du 8 novembre 2026) ---
    def _photo(self, couleur=(120, 90, 60)):
        p = self.tmp / f"photo-{couleur[0]}-{couleur[1]}-{couleur[2]}.jpg"
        if not p.exists():
            Image.new("RGB", (800, 1000), couleur).save(p)
        return str(p)

    def test_nouveaux_gabarits(self):
        cas = {
            "idee-recue.html": {"idee": "Il faut être musicien.", "titre": "Aucune compétence musicale n’est nécessaire.",
                                "texte": "On écoute, on joue, on chante comme on peut."},
            "chiffre.html": {"chiffre": "0", "titre": "compétence musicale",
                             "texte": "nécessaire pour venir en musicothérapie."},
            "citation.html": {"citation": "Même quand les mots se font rares, une mélodie familière peut encore "
                                          "faire naître un sourire.", "label": "Musique et personnes âgées"},
            "etapes.html": {"label": "Une pause pour soi", "titre": "Une minute d’écoute", "etape1": "Installez-vous",
                            "etape2": "Fermez les yeux", "etape3": "Comptez les sons autour de vous",
                            "etape4": "Rouvrez les yeux doucement"},
            "mots.html": {"mot1": "Écouter", "mot2": "Jouer", "mot3": "Chanter", "mot4": "Improviser",
                          "texte": "Quatre façons de vivre la musicothérapie."},
            "arche.html": {"label": "Coulisses", "titre": "Les bols chantants", "photo": self._photo(),
                           "texte": "Un son qui dure, qui vibre, qu’on sent autant qu’on l’entend."},
            "photo.html": {"label": "Dans la salle d’Enza", "titre": "Comment se passe une première séance ?",
                           "photo": self._photo()},
        }
        for nom, champs in cas.items():
            with self.subTest(gabarit=nom):
                p = rendre(G / nom, champs, self.tmp / nom.replace(".html", ".jpg"))
                with Image.open(p) as im:
                    self.assertEqual(im.size, (1080, 1350))

    def test_etapes_vides_masquees(self):  # une étape non remplie ne doit pas laisser de pastille numérotée
        p = rendre(G / "etapes.html", {"titre": "Test", "etape1": "Un", "etape2": "Deux"}, self.tmp / "etapes-2.jpg")
        with Image.open(p) as im:
            pastilles, dans = 0, False
            for y in range(250, 1300):
                r, g, b = im.getpixel((104, y))  # bord gauche des pastilles, à côté du chiffre
                miel = r > 140 and 90 < g < 150 and b < 90  # pastille dorée (#A87A2C)
                if miel and not dans:
                    pastilles += 1
                dans = miel
        self.assertEqual(pastilles, 2)

    def test_photo_obligatoire(self):
        with self.assertRaises(ValueError):
            rendre(G / "arche.html", {"titre": "Sans photo"}, self.tmp / "sans-photo.jpg")

    def test_photo_visible(self):
        p = rendre(G / "photo.html", {"titre": "Test", "photo": self._photo((255, 0, 0))}, self.tmp / "photo-rouge.jpg")
        with Image.open(p) as im:
            r, g, b = im.getpixel((540, 150))
        self.assertGreater(r, 200)
        self.assertLess(g, 60)

    def test_variante_creme(self):
        p = rendre(G / "diapo.html", {"titre": "Titre", "texte": "Texte", "variante": "creme"}, self.tmp / "creme.jpg")
        with Image.open(p) as im:
            r, g, b = im.getpixel((20, 20))
        self.assertGreater(min(r, g), 235)  # crème #FBF6E3, pas le vert de l'aquarelle
        self.assertGreater(b, 210)

    def test_variante_inconnue(self):
        with self.assertRaises(ValueError):
            rendre(G / "diapo.html", {"titre": "Titre", "variante": "violet"}, self.tmp / "violet.jpg")

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
