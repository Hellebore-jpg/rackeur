from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

from pathlib import Path # Gère les chemins de fichiers
import sqlite3 # Gère les intéractions avec les bases de données SQLite

# Seuls ces classes sont exportés avec "from sqlite_utils import *", tout le reste est interne au script.
__all__ = [
    'IndexedRow', 'DATA_DIR', 'DEFAULT_TABLE',
    'CREATE_FILE', 'TEMP_DB',
    'Database', 'DB_Reader',
]

IndexedRow = tuple[int, list[str]] # (Index réel de la ligne dans la BDD, Ligne)

DATA_DIR: Path = Path('assets/data/') # Dossier des fichiers SQLite
DEFAULT_TABLE: str = 'data' # Nom de la table utilisée par défaut