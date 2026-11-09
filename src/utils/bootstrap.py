from ..config import *
from .utils_config import *

def load_database() -> None:
    """Chargement de la base de données en fonction de son type.
    """
    global CSV, HEADERT, CATALOGUE, SESSION
    if CSV:
        HEADERT = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        CATALOGUE = Database()
    else:
        HEADERT = [str, float, str, int, str] # Changer pour utiliser du SQLite
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality']) # Changer pour utiliser du SQLite
        CATALOGUE = Database() # Changer pour utiliser du SQLite
    SESSION = Session()