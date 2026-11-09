from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPaintEvent, QResizeEvent
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget, QListView
)

from dataclasses import dataclass
from pathlib import Path
from typing import Final
import sys
import re

from src.utils.csv_utils import *
from src.utils.session_utils import *
import src.config as config

# CONFIG MANUELLE DE L'APP
BASE_DIR: Final[Path] = Path(__file__).parent
STYLESHEET_PATH: Final[Path] = BASE_DIR / "assets/style.qss"
CARD_WIDTH: Final[int] = 380

# CONFIG AUTO DE L'APP
HEADERT: list[type]
CATALOGUE: Database
SESSION: Session

# Fonctions helpers
def load_stylesheet() -> str:
    """Charge la feuille de style PyQt.

    Returns:
        str: Contenu de la feuille de style.
    """
    stylesheet = STYLESHEET_PATH.read_text(encoding="utf-8")
    def resolve_path(match):
        path = match.group(1).strip("\"'")
        absolute_path = (BASE_DIR / path).resolve()
        return f"url('{absolute_path.as_posix()}')"
    
    stylesheet = re.sub(
        r"url\((.*?)\)",
        resolve_path,
        stylesheet
    )
    
    return stylesheet

def make_card(content: QWidget) -> QFrame:
    """Crée un Widget dans une carte arondie avec une ombre.

    Args:
        content (QWidget): Widget à intégrer.

    Returns:
        QFrame: Carte avec widget intégré.
    """
    card = QFrame()
    card.setObjectName("card")
    card.setFixedWidth(CARD_WIDTH)
 
    layout = QVBoxLayout(card)
    layout.setContentsMargins(32, 32, 32, 32)
    layout.addWidget(content)
 
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(50)
    shadow.setOffset(0, 12)
    shadow.setColor(QColor(0, 0, 0, 160))
    card.setGraphicsEffect(shadow)
    return card

class BackgroundWidget(QWidget):
    """Crée l'arrière plan, garde la couleur du QSS en fallback.
    """
    
    def __init__(self, image_path: Path) -> None:
        """Charge l'image d'arrière plan.

        Args:
            image_path (Path): Chemin vers l'image d'arrière plan.
        """
        super().__init__()
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._pixmap: QPixmap = QPixmap(str(image_path))
        self._scaled: QPixmap = QPixmap()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        if not self._pixmap.isNull():
            self._scaled = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

    def paintEvent(self, event: QPaintEvent | None) -> None:
        super().paintEvent(event)
        if self._scaled.isNull():
            return
        painter = QPainter(self)
        x = (self.width() - self._scaled.width()) // 2
        y = (self.height() - self._scaled.height()) // 2
        painter.drawPixmap(x, y, self._scaled)
        painter.end()

def make_background(card: QFrame, bg_path: Path) -> QWidget:
    """Crée le widget d'arrière plan avec une carte au centre.

    Args:
        card (QFrame): Carte à mettre au centre.
        bg_path (Path): Chemin de l'image d'arrière plan.

    Returns:
        QWidget: Widget d'arrière plan.
    """
    root = BackgroundWidget(bg_path)
    root.setObjectName("root")
 
    layout = QVBoxLayout(root)
    layout.addStretch()
    layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
    layout.addStretch()
    return root
 
 
def make_header(title: str, subtitle: str) -> tuple[QLabel, QLabel]:
    """Crée une entête.

    Args:
        title (str): Titre de l'entête.
        subtitle (str): Sous titre de l'entête.

    Returns:
        tuple[QLabel, QLabel]: Entête.
    """
    title_label = QLabel(title)
    title_label.setObjectName("title")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setObjectName("subtitle")
    return title_label, subtitle_label

#=============================================================================#
# FENÊTRE DE SELECTION DU TYPE DE BASE DE DONNÉES                             #
#=============================================================================#
class SourceDialog(QDialog):
    """Fenêtre de séléction du type de base de données.
    """
    def __init__(self) -> None:
        """Crée la fenêtre de séléction du type de base de données.
        """
        super().__init__()
        self.setWindowTitle("Rackeur | Type de la base de données")
        self.setFixedSize(480, 420)
 
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
 
        title, subtitle = make_header("Type de données", "Choisissez le format de votre base de données")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(18)
 
        label = QLabel("Type")
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
 
        self.combo: QComboBox = QComboBox()
        self.combo.addItems(["CSV", "SQLite"])
        self.combo.setCursor(Qt.CursorShape.PointingHandCursor)
        view = QListView()
        self.combo.setView(view)
        popup = view.window()
        assert popup is not None
        popup.setWindowFlags(
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout.addWidget(self.combo)
        layout.addSpacing(22)
 
        self.continue_button: QPushButton = QPushButton("Continuer")
        self.continue_button.setObjectName("primaryButton")
        self.continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_button.clicked.connect(self.accept)
        layout.addWidget(self.continue_button)
 
        root = make_background(make_card(content), BASE_DIR / "assets/img/background.png")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)
 
    def is_csv(self) -> bool:
        return self.combo.currentText() == "CSV"

#=============================================================================#
# FENÊTRE DE CONNEXION / INSCRIPTION                                          #
#=============================================================================#
@dataclass(frozen=True)
class FieldSpec:
    key: str
    label: str
    placeholder: str
    is_password: bool = False
 
class FormPage(QWidget):
    """Fenêtre de connexion ou d'inscription avec nom d'utilisateur et mot de passe.
    """
 
    def __init__(self, title: str, subtitle: str, fields: list[FieldSpec], button_text: str, switch_text: str, link_text: str) -> None:
        """Initialise une fenêtre de connexion ou d'inscription avec les éléments spécifiés.

        Args:
            title (str): Titre de la fenêtre.
            subtitle (str): Sous-titre de la fenêtre.
            fields (list[FieldSpec]): Inputs à utiliser.
            button_text (str): Texte du bouton de validation.
            switch_text (str): Texte de changement de page (connexion <-> inscription)
            link_text (str): Texte de lien.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
 
        title_label, subtitle_label = make_header(title, subtitle)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(18)
 
        self.inputs: dict[str, QLineEdit] = {}
        self._password_inputs: list[QLineEdit] = []
 
        for spec in fields:
            field_label = QLabel(spec.label.upper())
            field_label.setObjectName("fieldLabel")
 
            edit = QLineEdit()
            edit.setPlaceholderText(spec.placeholder)
            if spec.is_password:
                edit.setEchoMode(QLineEdit.EchoMode.Password)
                self._password_inputs.append(edit)
 
            self.inputs[spec.key] = edit
            layout.addWidget(field_label)
            layout.addWidget(edit)
            layout.addSpacing(8)
 
        self.show_password: QCheckBox = QCheckBox("Afficher le mot de passe")
        self.show_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.show_password.toggled.connect(self._toggle_password)
        layout.addWidget(self.show_password)
        layout.addSpacing(14)
        self.message: QLabel = QLabel()
        self.message.setObjectName("messageLabel")
        self.message.setWordWrap(True)
        self.message.setTextFormat(Qt.TextFormat.RichText)
        self.message.hide()
        layout.addWidget(self.message)
        layout.addSpacing(10)
 
        self.submit_button: QPushButton = QPushButton(button_text)
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.submit_button)
        layout.addSpacing(10)
 
        switch_row = QHBoxLayout()
        switch_row.addStretch()
        switch_row.addWidget(QLabel(switch_text))
        self.switch_button: QPushButton = QPushButton(link_text)
        self.switch_button.setObjectName("linkButton")
        self.switch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        switch_row.addWidget(self.switch_button)
        switch_row.addStretch()
        layout.addLayout(switch_row)
 
    def _toggle_password(self, visible: bool) -> None:
        mode = QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        for edit in self._password_inputs:
            edit.setEchoMode(mode)
            
    def show_message(self, text: str, hints: list[str] | None = None) -> None:
        html = f"<b>{text}</b>"
        if hints:
            html += "<br>" + "<br>".join(f"• {hint}" for hint in hints)
        self.message.setText(html)
        self.message.show()

    def clear_message(self) -> None:
        self.message.hide()
        
class MainPage(QMainWindow):
    """Page principale affichée après la connexion.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rackeur | Catalogue")
        # Construire l'interface du tableau ici
        title, subtitle = make_header("Page principale", "Vous êtes connecté")
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setCentralWidget(make_background(make_card(content), BASE_DIR / "assets/img/background.png"))
            
class AuthWindow(QMainWindow):
    """Crée la fenêtre d'autentification en utilisant le template définit plus haut.
    """
    LOGIN_INDEX: Final[int] = 0
    REGISTER_INDEX: Final[int] = 1
 
    def __init__(self) -> None:
        """Initialise la page d'autentification.
        """
        super().__init__()
        self.setWindowTitle("Rackeur | Bienvenue")
        self.resize(520, 700)
        self.setMinimumSize(440, 640)
        self.main_page: MainPage | None = None
 
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
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
 
        self.setCentralWidget(make_background(make_card(self.stack), BASE_DIR / "assets/img/background.png"))
 
        self.login_page.switch_button.clicked.connect(
            lambda: self.show_page(self.REGISTER_INDEX)
        )
        self.register_page.switch_button.clicked.connect(
            lambda: self.show_page(self.LOGIN_INDEX)
        )
        self.login_page.submit_button.clicked.connect(self.on_login)
        self.register_page.submit_button.clicked.connect(self.on_register)
 
        self.show_page(self.LOGIN_INDEX)
 
    def show_page(self, index: int) -> None:
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
        self.main_page = MainPage()
        self.main_page.showMaximized()
        self.close()
 
    def on_login(self) -> None:
        page = self.login_page
        username: str = page.inputs["username"].text()
        password: str = page.inputs["password"].text()
        
        if SESSION.AUTH(username, password):
            self.open_main_page()
        else:
            page.inputs["password"].clear()
            page.show_message("Nom d'utilisateur ou mot de passe incorrect.")
 
    def on_register(self) -> None:
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
        
        leaks, length_ok, has_upper, has_digit, has_special = SESSION.SUGGEST_PWD_UPGRADE(password)
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
        
        if not SESSION.REGISTER(username, password, True):
            page.show_message("Ce nom d'utilisateur existe déjà.")
        if SESSION.USER_ID is not None:
            self.open_main_page()
        else:
            self.show_page(self.LOGIN_INDEX)
            page.show_message("Compte créé, mais la connexion a échoué. Réessayez.")

#=============================================================================#
# CHARGEMENT DE LA BASE DE DONNÉES EN FONCTION DU TYPE                        #
#=============================================================================#
def load_database() -> None:
    global HEADERT, CATALOGUE, SESSION
    if config.CSV:
        HEADERT = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        CATALOGUE = Database()
        SESSION = Session()
    else:
        HEADERT = [str, float, str, int, str] # Changer pour utiliser du SQLite
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality']) # Changer pour utiliser du SQLite
        CATALOGUE = Database() # Changer pour utiliser du SQLite
        SESSION = Session() # Changer pour utiliser du SQLite

#=============================================================================#
# DEMARRAGE DE L'APPLICATION                                                  #
#=============================================================================#
def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
 
    # Demande le type de BDD à l'utilisateur
    dialog = SourceDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted.value:
        return 0  # Quitter l'app si l'utilisateur ferme la fenêtre sans choisir
 
    # Charger la base de données
    config.CSV = dialog.is_csv()
    load_database()
 
    # Afficher la fenêtre de connexion
    window = AuthWindow()
    window.showMaximized()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())