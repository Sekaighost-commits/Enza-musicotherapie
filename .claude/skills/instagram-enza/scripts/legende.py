"""Vérificateur de légende pour les posts d'Enza (Instagram + Facebook).

Usage : python legende.py legende.txt [--sante]
  --sante : le post parle de santé ou de difficultés, le rappel
            « ne remplace pas l'avis d'un médecin » est alors obligatoire.
Code de sortie : 1 s'il reste un problème BLOQUANT, sinon 0.

Limite de hashtags : 5 par post ou reel, légende ET commentaires compris
(annonce du compte @creators d'Instagram le 18/12/2025, déploiement le
19/12/2025 ; vérifié le 2026-11-08). Si Instagram change la règle, modifier
MAX_HASHTAGS.
"""
import argparse
import re
import sys
import textwrap
import unicodedata
from dataclasses import dataclass
from pathlib import Path

MAX_HASHTAGS = 5
MAX_CARACTERES = 2200
APERCU = 125

_FORMES = r"(?:er|e|es|ent|ons|ez|é|ée|és|ées|er(?:a|ai|as|ons|ez|ont|ait|aient)|ait|aient)"
PROMESSES = [
    r"\bguéri(?!don)\w*",                          # guérir, guérie, guérirez, guérison… (pas « guéridon »)
    r"\bsoign" + _FORMES + r"\b",                  # « soins palliatifs », « soignants », « soigneusement » restent permis
    r"\btrait" + _FORMES + r"\b",                  # « traitement » reste permis
    r"\befficaces?\s+contre\b",
    r"\bmiracle\w*",
    r"\bmiraculeu\w*",
]
# Mots qui signalent un post « santé » : sans rappel, on prévient même sans --sante.
SANTE = re.compile(r"\b(?:deuil|anxi(?:été|eux|euse)s?|stress|burn-?out|dépression|alzheimer|maladies?|douleurs?|"
                   r"fin\s+de\s+vie|palliatifs?|troubles?|insomnies?|angoisses?|autisme|handicaps?|cancers?|démence)\b",
                   re.IGNORECASE)
URGENCES = [r"derni[eè]re\s+chance", r"offre\s+limitée", r"\bdépêchez", r"!!!"]
HASHTAG = re.compile(r"(?<!\S)#(?=[^\W\d_])\w+")
PONCTUATION_COLLEE = re.compile(r"[^\s\d  ][?!;:](?!//)")


@dataclass(frozen=True)
class Resultat:
    niveau: str   # "BLOQUANT" ou "ATTENTION"
    regle: str
    message: str


def _cherche(motifs, texte):
    for motif in motifs:
        m = re.search(motif, texte, re.IGNORECASE)
        if m:
            return m.group(0)
    return None


def verifier(texte: str, sante: bool = False) -> list[Resultat]:
    t = unicodedata.normalize("NFC", texte)
    res = []

    mot = _cherche(PROMESSES, t)
    if mot:
        res.append(Resultat("BLOQUANT", "promesse",
                            f"« {mot} » : promesse de guérison. Écrire plutôt accompagner, soutenir, apaiser, aider à exprimer."))
    rappel = (re.search(r"ne\s+remplace\s+pas", t, re.IGNORECASE)
              and re.search(r"médecin|spécialiste|médical", t, re.IGNORECASE))
    sujet_sante = SANTE.search(t)
    if sante and not rappel:
        res.append(Resultat("BLOQUANT", "rappel",
                            "Rappel manquant : « La musicothérapie accompagne, elle ne remplace pas "
                            "l'avis d'un médecin ou d'un spécialiste. »"))
    elif sujet_sante and not rappel:
        res.append(Resultat("ATTENTION", "rappel",
                            f"Le texte parle de santé (« {sujet_sante.group(0)} ») : ajouter le rappel médical "
                            "et relancer avec --sante."))
    tags = HASHTAG.findall(t)
    if len(tags) > MAX_HASHTAGS:
        res.append(Resultat("BLOQUANT", "hashtags",
                            f"{len(tags)} hashtags : {MAX_HASHTAGS} maximum (légende et commentaires compris)."))
    if len(t) > MAX_CARACTERES:
        res.append(Resultat("BLOQUANT", "longueur", f"{len(t)} caractères : {MAX_CARACTERES} maximum."))

    if re.search(r"musicothérapeute", t, re.IGNORECASE) and not re.search(r"en\s+formation", t, re.IGNORECASE):
        res.append(Resultat("ATTENTION", "statut",
                            "Si on parle d'Enza, écrire « musicothérapeute en formation »."))
    if re.search(r"https?://", t, re.IGNORECASE):
        res.append(Resultat("ATTENTION", "lien",
                            "Les liens ne sont pas cliquables sur Instagram : écrire l'adresse en clair "
                            "(musicotherapeute-hainaut.be) ou renvoyer au lien de la bio."))
    m = PONCTUATION_COLLEE.search(t)
    if m or '"' in t:
        detail = f"« {m.group(0)} »" if m else "guillemets droits"
        res.append(Resultat("ATTENTION", "typographie",
                            f"{detail} : espace insécable avant ? ! ; : et guillemets « »."))
    mot = _cherche(URGENCES, t)
    if mot:
        res.append(Resultat("ATTENTION", "urgence", f"« {mot} » : pas de fausse urgence, on invite sans presser."))
    fin = re.search(r"[.!?…](?:\s|$)|\n", t)
    premiere = t[:fin.end()] if fin else t
    if len(premiere.strip()) > APERCU:
        res.append(Resultat("ATTENTION", "apercu_coupe",
                            f"La première phrase dépasse {APERCU} caractères : elle sera coupée avant « … plus »."))
    return res


def apercu(texte: str) -> str:
    t = unicodedata.normalize("NFC", texte)
    return t if len(t) <= APERCU else t[:APERCU] + "… plus"


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Vérifie une légende de post pour le compte d'Enza.")
    p.add_argument("fichier", type=Path)
    p.add_argument("--sante", action="store_true", help="le post parle de santé ou de difficultés")
    args = p.parse_args(argv)
    texte = args.fichier.read_text(encoding="utf-8")

    print("CE QUE LE FIL MONTRE (avant « … plus »)")
    print("+" + "-" * 58 + "+")
    for ligne in textwrap.wrap(apercu(texte).replace("\n", " "), 56) or [""]:
        print(f"| {ligne:<56} |")
    print("+" + "-" * 58 + "+")
    resultats = verifier(texte, args.sante)
    for r in resultats:
        print(f"{r.niveau:<9} {r.regle:<13} {r.message}")
    if not resultats:
        print("OK        aucune remarque")
    return 1 if any(r.niveau == "BLOQUANT" for r in resultats) else 0


if __name__ == "__main__":
    sys.exit(main())
