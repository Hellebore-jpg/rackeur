from csv_utils import *

PERMISSSIONS: list[str] = [
    'Create', 'Read', 'Update', 'Delete'
]

class Session:
    """Gère les sessions utilisateur de manière sécurisée.
    """
    def __init__(self) -> None:
        """Crée une session vide, prête pour la connexion ou l'inscription.
        """
        self.DB: Database = Database('utilisateurs.csv')
        
        self.USER: str = 'Non Connécté'
        self.ID = -1
        self.PERMS: dict[bool] = {}
        
    def AUTH(self, username: str, password: str) -> bool:
        """Connecte un utilisateur et enregistre ses permissions dans la classe.

        Args:
            username (str): Nom d'utilisateur stocké en BDD.
            password (str): MDP en clair à comparer dans la BDD.

        Returns:
            bool: Succès de l'autentification.
        """
        reader: DB_Reader = DB_Reader(self.DB)
        reader.SEARCH(username, [0], True)
        reader.SELECT(0)
        user: list = reader.READ()
        if user[0] == username and user[1] == password:
            self.PERMS = {PERMISSSIONS[i]: (user[3][i] == "1") for i in range(len(PERMISSSIONS))}

if __name__ == '__main__':
    pass