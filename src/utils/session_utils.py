from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

from typing import NamedTuple # Permet de créer une classe pour définir un type de variable

import bcrypt # Hash des mots de passe (Identique à MySQL)

from . import utils_config, sqlite_utils, csv_utils
from .api_utils import PWNED_COUNT

# Seuls ces classes sont exportés avec "from session_utils import *", tout le reste est interne au script.
__all__ = [
    'PwdCheckResult', 'LOGGED_OUT', 'PERMISSIONS',
    'Session',
]

class PwdCheckResult(NamedTuple):
    leaks: int
    length_8: bool
    has_upper: bool
    has_digit: bool
    has_special: bool

LOGGED_OUT: list[str] = ['Non Connécté', '*****', 'none', '00000']
PERMISSIONS: list[str] = ['CREATE', 'READ', 'UPDATE', 'DELETE', 'USER']
NO_PERMS = {e: False for e in PERMISSIONS}

HEADER_TYPE: list[type] = [str]

def _password(password: str) -> str:
    """Renvoie le hash du mot de passe.

    Args:
        password (str): Mot de passe en clair.

    Returns:
        str: Mot de passe hashé.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def _verify(password: str, stored: str) -> bool:
    """Renvoie true si le mot de passe correspond au hash.

    Args:
        password (str): Mot de passe en clair.
        stored (str): Hash stocké en BDD.

    Returns:
        bool: Validité du mot de passe.
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), stored.encode('utf-8'))
    except ValueError: # Hash invalide
        return False

class Session:
    """Gère les sessions utilisateur de manière sécurisée.
    """
    def __init__(self) -> None:
        """Crée une session vide, prête pour la connexion ou l'inscription.
        """
        self.DB: csv_utils.Database | sqlite_utils.Database
        if utils_config.CSV:
            csv_utils.CREATE_FILE("utilisateurs.csv", ['username', 'password', 'role', 'permissions'])
            self.DB = csv_utils.Database('utilisateurs.csv')
        else:
            self.DB = sqlite_utils.Database('utilisateurs.db')
        if self.DB.BODY == []:
            self.DB.CREATE(["admin", "$2b$12$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe", 'admin', '11111'])
            self.DB.CREATE(["editor", "$2b$12$ruxeVHj1j5e3UPwHvbCMyufY/qinDTxo2liFTlvcr7nXEva.qqhKe", 'editor', '01100'])
            if utils_config.CSV: self.DB.SAVE_FILE()
        
        self.USER: list[str] = list(LOGGED_OUT)
        self.USER_ID: int | None = None
        self.PERMS: dict[str, bool] = NO_PERMS
        
    def __find(self, username: str) -> csv_utils.IndexedRow | sqlite_utils.IndexedRow | None:
        """Cherche un utilisateur par son nom exact.

        Args:
            username (str): Nom d'utilisateur.

        Returns:
            IndexedRow | None: (index, ligne) ou None si introuvable.
        """
        if utils_config.CSV:
            matches: list[csv_utils.IndexedRow] = self.DB.READER().SEARCH(username, [0], True).BODY
        else:
            matches: list[sqlite_utils.IndexedRow] = self.DB.READER().SEARCH(username, [0], True).BODY
        return matches[0] if matches else None
        
    def AUTH(self, username: str, password: str) -> bool:
        """Connecte un utilisateur et enregistre ses permissions dans la classe.

        Args:
            username (str): Nom d'utilisateur stocké en BDD.
            password (str): MDP en clair à comparer dans la BDD.

        Returns:
            bool: Succès de l'autentification.
        """
        found: csv_utils.IndexedRow | sqlite_utils.IndexedRow | None = self.__find(username)
        if found is None:
            return False
        id, row = found
        if len(row) < 4 or not _verify(password, row[1]):
            return False
        perms: dict[str, bool] = {p: row[3][i:i + 1] == '1' for i, p in enumerate(PERMISSIONS)}
        # La session est initialisée
        self.USER_ID = id
        self.USER = row
        self.PERMS = perms
        return True
    
    def REGISTER(self, username: str, password: str, autoconnect: bool = False) -> bool:
        """Inscrit un utilisateur et enregistre ses données dans la base de données.
    
        Args:
            username (str): Nom d'utilisateur.
            password (str): MDP en clair.
            autoconnect (bool): L'utilisateur se fait connecter tout de suite après l'inscription au lieu de rentrer son mdp à nouveau.
    
        Returns:
            bool: Succès de l'inscription.
        """
        if self.__find(username) is not None:
            return False
        self.DB.CREATE([username, _password(password), 'visiteur', '0100'])
        if isinstance(self.DB, csv_utils.Database):
            self.DB.SAVE_FILE()
        if autoconnect:
            self.AUTH(username, password)
        return True
        
    def LOG_OUT(self) -> None:
        self.USER = list(LOGGED_OUT)
        self.USER_ID = None
        self.PERMS = NO_PERMS
        
    def CHECK_PERM(self, perm: str = 'CREATE') -> bool:
        """Renvoie si l'utilisateur possède la permission demandée.

        Args:
            perm (str, optional): Permission requise, doit être présente dans la liste PERMISSIONS. Defaults to 'CREATE'.

        Returns:
            bool: Utilisateur autorisé.
        """
        return self.PERMS.get(perm.upper(), False)
    
    def SUGGEST_PWD_UPGRADE(self, password: str) -> PwdCheckResult:
        """Renvoie une liste détaillant la robustesse du mot de passe à appeller avant d'inscrire l'utilisateur ou de changer son mdp pour lui suggérer un mdp plus robuste.

        Args:
            password (str): Mot de passe en clair.

        Returns:
            PwdCheckResult: [Nombre de leaks, 8 caractères minimum, Majuscules, Chiffres, Charactères Spéciaux]
        """
        leaks = PWNED_COUNT(password)
        length_8 = len(password) >= 8
        has_upper = any(char.isupper() for char in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not char.isalnum() for char in password)
        return  PwdCheckResult(leaks, length_8, has_upper, has_digit, has_special)