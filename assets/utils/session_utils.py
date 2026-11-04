from csv_utils import Catalogue, Catalogue_Reader, CREATE_FILE

class Session:
    """Gère les sessions utilisateur de manière sécurisée.
    """
    def __init__(self) -> None:
        """Crée une session vide, prête pour la connexion ou l'inscription.
        """
        self.USER: str = 'Logged Out'
        self.perm_format: str = 'CRUD'
        self.PERMS: dict = {}

if __name__ == '__main__':
    pass