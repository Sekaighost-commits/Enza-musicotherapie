"""Le skill contient bien chaque règle clé de la conception, et ses renvois mènent à des fichiers réels."""
import re
import unittest
from pathlib import Path

RACINE_SKILL = Path(__file__).resolve().parents[1]
RACINE_SITE = RACINE_SKILL.parents[2]
DOSSIER_TRAVAIL = Path.home() / "Documents" / "Instagram-Enza"   # journal.md vit ici, hors du site

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


def lire(nom):
    return (RACINE_SKILL / nom).read_text(encoding="utf-8")


class TestContenuSkill(unittest.TestCase):
    def test_phrases_cles(self):
        for fichier, phrases in ATTENDUS.items():
            texte = lire(fichier)
            for phrase in phrases:
                self.assertIn(phrase, texte, f"{fichier} : « {phrase} » manque")

    def test_frontmatter(self):
        texte = lire("SKILL.md")
        m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
        self.assertIsNotNone(m, "SKILL.md doit commencer par un frontmatter")
        self.assertRegex(m.group(1), r"(?m)^name: instagram-enza$")
        self.assertRegex(m.group(1), r"(?m)^description: .{80,}$")

    def test_renvois_existent(self):
        texte = lire("SKILL.md")
        cites = set(re.findall(r"`([\w./-]+\.(?:md|py|html|css))`", texte))
        self.assertTrue(cites, "SKILL.md ne cite aucun fichier")
        for nom in cites:
            self.assertTrue(any((d / nom).exists() for d in (RACINE_SKILL, RACINE_SITE, DOSSIER_TRAVAIL)),
                            f"{nom} introuvable")


if __name__ == "__main__":
    unittest.main()
