from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

from pathlib import Path # Gère les chemins de fichiers
import sqlite3 # Gère les intéractions avec les bases de données SQLite

# Seuls ces classes sont exportés avec "from sqlite_utils import *", tout le reste est interne au script.
__all__ = [
]

DATA_DIR: Path = Path('assets/data/') # Dossier des fichiers SQlite

def CREATE_PATH() -> None:
    """Crée un répertoire vide "assets/data/" si il n'existe pas.
    """
    if DATA_DIR.exists(): return # Arrête si le chemin existe déjà
    DATA_DIR.parent.mkdir(parents=True, exist_ok=True) # Crée les dossiers manquants
    
db = sqlite3.connect(DATA_DIR / 'catalogue.db')