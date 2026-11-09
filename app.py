from src.utils.utils_config import *
from src.utils.bootstrap import *
from src.utils.helpers import *
from src.config import *

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
        self.setFixedSize(480, 600)
 
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
 
        root = make_background(make_card(content), RoundedImage(USER_PLACEHOLDER_PATH))
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
        self.setCentralWidget(make_background(make_card(content), RoundedImage(USER_PLACEHOLDER_PATH)))
            
class AuthWindow(QMainWindow):
    """Crée la fenêtre d'autentification en utilisant le template définit plus haut.
    """
    LOGIN_INDEX: int = 0
    REGISTER_INDEX: int = 1
 
    def __init__(self) -> None:
        """Initialise la page d'autentification.
        """
        super().__init__()
        self.setWindowTitle("Rackeur | Bienvenue")
        self.resize(520, 820)
        self.setMinimumSize(440, 820)
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
 
        self.setCentralWidget(make_background(make_card(self.stack), RoundedImage(USER_PLACEHOLDER_PATH)))
 
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

class SplashDialog(QDialog):
    """Écran titre : fondu entrant, pause, fondu sortant (2s), passer en appuyant sur la touche Entrer.
    """
    
    FADE_MS: int = 500
    HOLD_MS: int = 3000

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("The Rackeur")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowState(Qt.WindowState.WindowMaximized)

        font_id = QFontDatabase.addApplicationFont(str(FONT_PATH))
        families = QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else []

        title = QLabel("The Rackeur")
        title.setObjectName("splashTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if families:
            title.setFont(QFont(families[0]))

        icon = QLabel()
        icon.setPixmap(
            QPixmap(str(ICON_PATH)).scaled(
                400, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.addWidget(title)
        content_layout.addWidget(icon)

        self._effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(content)
        self._effect.setOpacity(0.0)
        content.setGraphicsEffect(self._effect)

        root = BackgroundWidget(BACKGROUND_PATH)
        root_layout = QVBoxLayout(root)
        root_layout.addStretch()
        root_layout.addWidget(content, alignment=Qt.AlignmentFlag.AlignHCenter)
        root_layout.addStretch()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)

        fade_in = QPropertyAnimation(self._effect, b"opacity", self)
        fade_in.setDuration(self.FADE_MS)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)

        fade_out = QPropertyAnimation(self._effect, b"opacity", self)
        fade_out.setDuration(self.FADE_MS)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)

        self._anim: QSequentialAnimationGroup = QSequentialAnimationGroup(self)
        self._anim.addAnimation(fade_in)
        self._anim.addPause(self.HOLD_MS)
        self._anim.addAnimation(fade_out)
        self._anim.finished.connect(self.accept)

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self.activateWindow()
        self.setFocus()
        self._anim.start()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event is not None and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._anim.stop()
            self.accept()
            return
        super().keyPressEvent(event)

#=============================================================================#
# DEMARRAGE DE L'APPLICATION                                                  #
#=============================================================================#
def main() -> int:
    global CSV
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(FAVICON_PATH)))
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
 
    # Demande le type de BDD à l'utilisateur
    dialog = SourceDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted.value:
        return 0  # Quitter l'app si l'utilisateur ferme la fenêtre sans choisir
 
    # Charger la base de données
    CSV = dialog.is_csv()
    load_database()
    
    SplashDialog().exec()
 
    # Afficher la fenêtre de connexion
    window = AuthWindow()
    window.showMaximized()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())