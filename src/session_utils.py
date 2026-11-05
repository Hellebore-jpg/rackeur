from typing import NamedTuple

import bcrypt # Hash des mots de passe (Identique à MySQL)

from .csv_utils import *
from .api_utils import *

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

LOGGED_OUT: list[str] = ['Non Connécté', '*****', 'none', '0000']
PERMISSIONS: list[str] = ['CREATE', 'READ', 'UPDATE', 'DELETE']
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
        self.DB: Database = Database('utilisateurs.csv')
        
        self.USER: list[str] = list(LOGGED_OUT)
        self.USER_ID: int | None = None
        self.PERMS: dict[str, bool] = NO_PERMS
        
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
        
# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------

def TESTING() -> None:
    """Teste le module de session sur une base d'utilisateurs temporaire. Lève une AssertionError au premier test qui échoue.
    """
    header: list[str] = ['username', 'password', 'role', 'permissions']
    visitor_perms: dict[str, bool] = {'CREATE': False, 'READ': True, 'UPDATE': False, 'DELETE': False} # '0100'
    passed: int = 0

    def check(name: str, got: object, expected: object) -> None:
        nonlocal passed
        assert got == expected, f'[FAIL] {name}\n  obtenu  : {got!r}\n  attendu : {expected!r}'
        passed += 1
        print(f'[ OK ] {name}')

    # 1. Hash des mots de passe
    h1: str = _password('secret')
    h2: str = _password('secret')
    check('le hash ne contient pas le mot de passe', 'secret' in h1, False)
    check('deux hash du même mot de passe sont différents (sel)', h1 != h2, True)
    check('_verify : bon mot de passe', _verify('secret', h1), True)
    check('_verify : mauvais mot de passe', _verify('Secret', h1), False)
    check('_verify : hash invalide -> False sans erreur', _verify('secret', 'pas-un-hash'), False)

    with TEMP_DB(header, []) as db:
        s: Session = Session()
        s.DB = db

        # 2. État initial
        check('USER initial = LOGGED_OUT', s.USER, LOGGED_OUT)
        check('USER est une copie de LOGGED_OUT', s.USER is not LOGGED_OUT, True)
        check('USER_ID initial = None', s.USER_ID, None)
        check('PERMS initiales toutes à False', s.PERMS, NO_PERMS)

        # 3. Inscription
        check('REGISTER : nouvel utilisateur', s.REGISTER('rateau', 'pw-rateau'), True)
        saved: Database = Database(db.PATH) # Relecture du fichier pour vérifier la sauvegarde
        check('REGISTER : ligne sauvegardée dans le fichier', len(saved.BODY), 1)
        check('REGISTER : nom, rôle et permissions par défaut', [saved.BODY[0][0], saved.BODY[0][2], saved.BODY[0][3]], ['rateau', 'visiteur', '0100'])
        check('REGISTER : mot de passe stocké hashé', saved.BODY[0][1] != 'pw-rateau' and _verify('pw-rateau', saved.BODY[0][1]), True)
        check('REGISTER : doublon refusé', s.REGISTER('rateau', 'autre'), False)
        check('REGISTER : le doublon n\'ajoute pas de ligne', len(Database(db.PATH).BODY), 1)
        check('REGISTER : le doublon ne remplace pas le mot de passe', _verify('pw-rateau', Database(db.PATH).BODY[0][1]), True)

        # 4. Connexion
        check('AUTH : inconnu -> False sans erreur', s.AUTH('personne', 'x'), False)
        check('AUTH : mauvais mot de passe', s.AUTH('rateau', 'faux'), False)
        check('AUTH : un échec ne modifie pas la session', (s.USER, s.USER_ID, s.PERMS), (LOGGED_OUT, None, NO_PERMS))
        check('AUTH : succès', s.AUTH('rateau', 'pw-rateau'), True)
        check('AUTH : USER_ID = index réel', s.USER_ID, 0)
        check('AUTH : nom de l\'utilisateur', s.USER[0], 'rateau')
        check('AUTH : permissions chargées', s.PERMS, visitor_perms)

        # 5. Plusieurs utilisateurs : index réels et isolation
        s.REGISTER('rater', 'pw-rater')
        s.REGISTER('rat_thon', 'pw-rat_thon')
        check('AUTH : USER_ID du 3e utilisateur = 2', s.AUTH('rat_thon', 'pw-rat_thon'), True)
        check('AUTH : index réel conservé', s.USER_ID, 2)
        check('AUTH : mot de passe d\'un autre utilisateur refusé', s.AUTH('rater', 'pw-rat_thon'), False)
        check('AUTH : un échec ne déconnecte pas l\'utilisateur actuel', (s.USER[0], s.USER_ID), ('rat_thon', 2))

        # 6. Déconnexion
        s.LOG_OUT()
        check('LOG_OUT : USER', s.USER, LOGGED_OUT)
        check('LOG_OUT : USER n\'est pas la liste globale (check du bug des listes "partagées")', s.USER is not LOGGED_OUT, True)
        check('LOG_OUT : USER_ID', s.USER_ID, None)
        check('LOG_OUT : PERMS', s.PERMS, NO_PERMS)

        # 7. Lignes corrompues dans le fichier : ne doivent jamais faire planter AUTH
        db.CREATE(['ghost', 'pas-un-hash'])  # Ligne trop courte
        check('AUTH : ligne trop courte -> False', s.AUTH('ghost', 'x'), False)
        db.CREATE(['dave', _password('pw-dave'), 'visiteur', '01'])  # Permissions trop courtes
        check('AUTH : permissions trop courtes -> pas d\'erreur', s.AUTH('dave', 'pw-dave'), True)
        check('AUTH : permissions manquantes = False', s.PERMS, {'CREATE': False, 'READ': True, 'UPDATE': False, 'DELETE': False})
        
        # 8. Check des permissions
        db.CREATE(['admin', _password('pw-admin'), 'admin', '1111'])
        s.LOG_OUT()
        check('CHECK_PERM : déconnecté -> tout refusé', [s.CHECK_PERM(p) for p in PERMISSIONS], [False] * 4)
        s.AUTH('rateau', 'pw-rateau') # Permissions '0100' : lecture seule
        check('CHECK_PERM : permission accordée', s.CHECK_PERM('READ'), True)
        check('CHECK_PERM : permission refusée', s.CHECK_PERM('DELETE'), False)
        check('CHECK_PERM : valeur par défaut (CREATE) refusée', s.CHECK_PERM(), False)
        check('CHECK_PERM : insensible à la casse', (s.CHECK_PERM('read'), s.CHECK_PERM('Read'), s.CHECK_PERM('rEaD')), (True, True, True))
        check('CHECK_PERM : permission inconnue -> False', s.CHECK_PERM('FLY'), False)
        s.AUTH('admin', 'pw-admin') # Permissions '1111' : tout autorisé
        check('CHECK_PERM : administrateur autorisé partout', [s.CHECK_PERM(p) for p in PERMISSIONS], [True] * 4)
        s.LOG_OUT()
        check('CHECK_PERM : LOG_OUT retire les droits', s.CHECK_PERM('READ'), False)

    print(f'\n{passed} tests réussis.')

if __name__ == '__main__':
    TESTING()