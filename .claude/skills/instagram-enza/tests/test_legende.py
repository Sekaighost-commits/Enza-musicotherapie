"""Tests du vérificateur de légende (scripts/legende.py)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from legende import MAX_HASHTAGS, apercu, verifier  # noqa: E402

LEGENDE_PY = SCRIPTS / "legende.py"
RAPPEL = "La musicothérapie accompagne, elle ne remplace pas l'avis d'un médecin ou d'un spécialiste."


def regles(texte, sante=False):
    return {r.regle for r in verifier(texte, sante)}


def bloquants(texte, sante=False):
    return {r.regle for r in verifier(texte, sante) if r.niveau == "BLOQUANT"}


def lancer(texte, *options):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "legende.txt"
        f.write_text(texte, encoding="utf-8")
        return subprocess.run([sys.executable, str(LEGENDE_PY), str(f), *options],
                              capture_output=True, text=True, encoding="utf-8")


class TestLegende(unittest.TestCase):
    def test_promesse_bloquee(self):
        for t in ["La musique soigne l'anxiété.", "Elle peut guérir le stress.", "Un effet miracle.",
                  "C'est efficace contre l'insomnie.", "On va traiter vos angoisses."]:
            self.assertIn("promesse", bloquants(t), t)

    def test_soins_palliatifs_et_traitement_autorises(self):
        t = "En soins palliatifs, la musique apaise. " + RAPPEL + " Elle ne remplace pas un traitement."
        self.assertNotIn("promesse", regles(t, sante=True))

    def test_accents_decomposes(self):  # Review Focus 1
        self.assertIn("promesse", bloquants("Pour guérir vite."))

    def test_rappel_obligatoire_si_sante(self):
        self.assertIn("rappel", bloquants("Le deuil se vit en musique.", sante=True))
        self.assertNotIn("rappel", regles("Le deuil se vit en musique. " + RAPPEL, sante=True))
        self.assertNotIn("rappel", regles("Atelier samedi à Vaulx.", sante=False))

    def test_hashtags(self):  # Review Focus 5
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
        self.assertNotIn("typographie", regles("Pour qui ? Rendez-vous à 10:30."))
        self.assertIn("urgence", regles("Dernière chance, dépêchez-vous !!!"))

    def test_apercu(self):
        self.assertEqual(apercu("Court."), "Court.")
        self.assertTrue(apercu("x" * 200).endswith("… plus"))
        self.assertEqual(len(apercu("x" * 200)), 125 + len("… plus"))

    def test_cli_code_sortie(self):
        self.assertEqual(lancer("La musique soigne.").returncode, 1)
        self.assertEqual(lancer("Atelier à Vaulx. " + RAPPEL, "--sante").returncode, 0)


if __name__ == "__main__":
    unittest.main()
