import hashlib
import hmac # Comparaison de hash

from csv_utils import *

LOGGED_OUT: list[str] = ['Non Connécté', '*****', 'none', '0000']
PERMISSSIONS: list[str] = ['Create', 'Read', 'Update', 'Delete']

HEADER_TYPE: list[type] = [str]

def _password(password: str) -> str:
    """Renvoie le hash du mot de passe.

    Args:
        password (str): Mot de passe en clair.

    Returns:
        str: Mot de passe hashé.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class Session:
    """Gère les sessions utilisateur de manière sécurisée.
    """
    def __init__(self) -> None:
        """Crée une session vide, prête pour la connexion ou l'inscription.
        """
        self.DB: Database = Database('utilisateurs.csv')
        
        self.USER: list[str] = list(LOGGED_OUT)
        self.USER_ID: int | None = None
        self.PERMS: dict[str, bool] = {e: False for e in PERMISSSIONS}
        
    def __find(self, username: str) -> IndexedRow | None:
        """Cherche un utilisateur par son nom exact.

        Args:
            username (str): Nom d'utilisateur.

        Returns:
            IndexedRow | None: (index, ligne) ou None si introuvable.
        """
        matches: list[IndexedRow] = self.DB.READER().SEARCH(username, [0], True).BODY
        return matches[0] if matches else None
        
    def AUTH(self, username: str, password: str) -> bool:
        """Connecte un utilisateur et enregistre ses permissions dans la classe.

        Args:
            username (str): Nom d'utilisateur stocké en BDD.
            password (str): MDP en clair à comparer dans la BDD.

        Returns:
            bool: Succès de l'autentification.
        """
        found: IndexedRow | None = self.__find(username)
        if found is None:
            return False
        id, row = found
        if len(row) < 4 or not hmac.compare_digest(row[1], _password(password)):
            return False
        self.USER_ID = id # La session est initialisée
        self.USER = row
        self.PERMS = {PERMISSSIONS[i]: row[3][i] == '1' for i in range(len(PERMISSSIONS))}
        return True
    
    def REGISTER(self, username: str, password: str) -> bool:
        """Inscrit un utilisateur et enregistre ses données dans la base de données.
    
        Args:
            username (str): Nom d'utilisateur.
            password (str): MDP en clair.
    
        Returns:
            bool: Succès de l'inscription.
        """
        if self.__find(username) is not None:
            return False
        self.DB.CREATE([username, _password(password), 'visiteur', '0100'])
        self.DB.SAVE_FILE()
        return True
        
    def LOG_OUT(self) -> None:
        self.USER = list(LOGGED_OUT)
        self.USER_ID = None
        self.PERMS = {e: False for e in PERMISSSIONS}

if __name__ == '__main__':
    pass