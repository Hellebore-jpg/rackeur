from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QSizePolicy, QStackedWidget,
)
from PyQt6.QtGui import QKeyEvent

from ..utils.helpers import make_background, make_card, RoundedImage, Page
from .. import config

#=============================================================================#
# IMPORTATION DES FENÊTRES                                                    #
#=============================================================================#
from src.ui.form_page import FormPage, FieldSpec
from src.ui.main_page import MainPage
from src.ui.splash import SplashDialog

class AuthWindow(Page):
    """Crée la fenêtre d'autentification en utilisant le template définit plus haut.
    """
    LOGIN_INDEX: int = 1
    REGISTER_INDEX: int = 2
    TYPE_AUTH: bool = False
 
    def __init__(self, app_window) -> None:
        """Initialise la page d'autentification.
        """
        super().__init__()
        self.app_window = app_window
        self.setWindowTitle("Rackeur | Bienvenue")
        self.resize(520, 820)
        self.setMinimumSize(440, 820)
        self.main_page: MainPage | None = None
        self.next: bool = True
 
        self.login_page: FormPage = FormPage(
            "Connexion",
            "Connectez vous pour continuer",
            [
                FieldSpec("username", "Nom d'utilisateur", "nom_d_utilisateur"),
                FieldSpec("password", "Mot de passe", "m0T 2 P4s2e", True),
            ],
            "Se connecter",
            "Vous n'avez pas de compte ?",
            "S'inscrire",
        )
        self.register_page: FormPage = FormPage(
            "Inscription",
            "Créez un compte pour démarrer",
            [
                FieldSpec("username", "Nom d'utilisateur", "nom_d_utilisateur"),
                FieldSpec("password", "Mot de passe", "m0T 2 P4s2e", True),
                FieldSpec("confirm", "Confirmez le mot de passe", "m0T 2 P4s2e", True),
            ],
            "S'inscrire",
            "Vous avez déjà un compte ?",
            "Se connecter",
        )

        self.stack: QStackedWidget = QStackedWidget()
        self.splash = SplashDialog()
        self.stack.addWidget(self.splash)
        self.stack.addWidget(make_background(make_card(self.login_page), RoundedImage(config.USER_PLACEHOLDER_PATH)))
        self.stack.addWidget(make_background(make_card(self.register_page), RoundedImage(config.USER_PLACEHOLDER_PATH)))

        self.setCentralWidget(self.stack)
         
        self.login_page.switch_button.clicked.connect(lambda: self.show_page(self.REGISTER_INDEX))
        self.register_page.switch_button.clicked.connect(lambda: self.show_page(self.LOGIN_INDEX))
        self.login_page.submit_button.clicked.connect(self.on_login)
        self.register_page.submit_button.clicked.connect(self.on_register)

        self.splash.finished.connect(lambda: self.show_page(self.LOGIN_INDEX))
        self.stack.setCurrentWidget(self.splash)

    def show_page(self, index: int) -> None:
        """Charge une autre page.

        Args:
            index (int): Index de la page définit dans la classe.
        """
        if index == 1:
            TYPE_AUTH = False
        if index == 2:
            TYPE_AUTH = True
        for i in range(self.stack.count()):
            policy = (
                QSizePolicy.Policy.Preferred
                if i == index
                else QSizePolicy.Policy.Ignored
            )
            self.stack.widget(i).setSizePolicy(policy, policy) # type: ignore[union-attr]
        self.stack.setCurrentIndex(index)
        self.stack.updateGeometry()
        self.login_page.clear_message()
        self.register_page.clear_message()
        
    def open_main_page(self) -> None:
        from src.ui.main_page import MainPage
        self.app_window.switch_to("main",lambda window: MainPage(window),)

 
    def on_login(self) -> None:
        """Fonction de comportement du bouton de connexion.
        """
        page = self.login_page
        username: str = page.inputs["username"].text()
        password: str = page.inputs["password"].text()
        
        if config.SESSION.AUTH(username, password):
            if self.next == False:
                self.open_main_page()
            leaks, _, _, _, _ = config.SESSION.SUGGEST_PWD_UPGRADE(password)
            if leaks > 0:
                page.show_message(f"Ce mot de passe a déjà fuité {leaks} fois dans des bases piratées. Changez-le !")
                self.login_page.submit_button.setText("Se connecter quand même")
                self.login_page.submit_button.setStyleSheet("background-color: #e74c3c")
            self.next = False
        else:
            page.inputs["password"].clear()
            page.show_message("Nom d'utilisateur ou mot de passe incorrect.")
 
    def on_register(self) -> None:
        """Fonction de comportement du bouton d'inscription.
        """
        page = self.register_page
        username: str = page.inputs["username"].text().strip()
        password: str = page.inputs["password"].text()
        confirm: str = page.inputs["confirm"].text()
        
        if not username:
            page.show_message("Choisissez un nom d'utilisateur.")
            return
        if password != confirm:
            page.show_message("Les mots de passe ne correspondent pas.")
            return
        
        leaks, length_ok, has_upper, has_digit, has_special = config.SESSION.SUGGEST_PWD_UPGRADE(password)
        hints: list[str] = []
        if leaks > 0:
            hints.append(f"Ce mot de passe a déjà fuité {leaks} fois dans des bases piratées")
        if not length_ok:
            hints.append("Utilisez au moins 8 caractères")
        if not has_upper:
            hints.append("Ajoutez une majuscule")
        if not has_digit:
            hints.append("Ajoutez un chiffre")
        if not has_special:
            hints.append("Ajoutez un caractère spécial (! ? # @ ...)")
        if hints:
            page.show_message("Mot de passe trop faible :", hints)
            return
        
        if not config.SESSION.REGISTER(username, password, True):
            page.show_message("Ce nom d'utilisateur existe déjà.")
        if config.SESSION.USER_ID is not None:
            self.open_main_page()
        else:
            self.show_page(self.LOGIN_INDEX)
            page.show_message("Compte créé, mais la connexion a échoué. Réessayez.")

    def keyPressEnter(self, event: QKeyEvent | None) -> None:
        """Permet de se connecter ou de s'inscrire "Entrée"
        
        Args:
            event (QKeyEvent | None): Evénement lié à la touche.
            type_auth (bool): Variable qui permet de différencier une connexion d'une inscription.
        """
        if event is not None and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.TYPE_AUTH == False:
                self.on_login
            if self.TYPE_AUTH == True:
                self.on_register
        super().keyPressEvent(event)