from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

from .. import config
from .session_utils import Session
from . import utils_config, csv_utils, sqlite_utils

def load_database() -> None:
    """Chargement de la base de données en fonction de son type.
    """
    if utils_config.CSV:
        config.HEADERT = [str, float, str, int, str]
        csv_utils.CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        config.CATALOG = csv_utils.Database()
    else:
        sqlite_utils.CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        config.CATALOG = sqlite_utils.Database(table="catalogue.db")
    config.SESSION = Session()