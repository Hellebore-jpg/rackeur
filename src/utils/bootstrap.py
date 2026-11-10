from __future__ import annotations

from .. import config
from .session_utils import Session
from .utils_config import CSV
from .csv_utils import CREATE_FILE, Database

def load_database() -> None:
    """Chargement de la base de données en fonction de son type.
    """
    if CSV:
        config.HEADERT = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        config.CATALOG = Database()
    else:
        config.HEADERT = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        config.CATALOG = Database()
    config.SESSION = Session()   