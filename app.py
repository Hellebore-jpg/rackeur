<<<<<<< HEAD
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                            QPushButton, QWidget, QPushButton, 
                            QListWidget, QHBoxLayout, QVBoxLayout, 
                            QFrame, QLabel, QLineEdit, QHeaderView,
                            QMenu, QCheckBox, QComboBox,
                            QDateEdit, QDateTimeEdit, QStackedLayout,
                            QDial, QDoubleSpinBox, QFontComboBox,
                            QLabel, QLCDNumber, QLineEdit,
                            QMainWindow, QProgressBar, QPushButton,
                            QRadioButton, QSlider, QSpinBox,
                            QTimeEdit, QVBoxLayout, QWidget, QGridLayout, QTableView)
from PyQt6.QtCore import QSize, Qt, QRect, QPropertyAnimation
from PyQt6.QtGui import QAction, QColor, QPalette
import sys
from src import api_utils, csv_utils, session_utils
from src.session_utils import Session
from src.csv_utils import Database
from product_model import ProduitModel
from random import choice
from layout_colorwidget import Color

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle("My App")
        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        connexion_layout = QVBoxLayout()
        inscription_layout = QVBoxLayout()
        catalog_layout = QVBoxLayout()

        page_layout.addLayout(button_layout)
        page_layout.addLayout(self.stacklayout)

        self.session = Session()

        titre = QLabel("Bienvenue sur Racker !")
        titre.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        titre.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        connexion_layout.addWidget(titre)
        label = QLabel("Entrez vos identifiants et mot de passe : ")
        label.setStyleSheet("font-size: 18px; color: white;")
        connexion_layout.addWidget(label)
        self.user_id_connexion = QLineEdit()
        self.user_id_connexion.setPlaceholderText("Identifiant")
        self.user_id_connexion.setStyleSheet("font-size: 18px; color: white;")
        self.user_id_connexion.textChanged.connect(lambda texte: print("Identifiant modifié :", repr(texte)))
        connexion_layout.addWidget(self.user_id_connexion)
        self.password_connexion = QLineEdit()
        self.password_connexion.setPlaceholderText("Mot de passe")
        self.password_connexion.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_connexion.setStyleSheet("font-size: 18px; color: white;")
        self.password_connexion.textChanged.connect(lambda texte: print("Mot de passe modifié :", repr(texte)))
        connexion_layout.addWidget(self.password_connexion)
        btn = QPushButton("Se Connecter")
        btn.setStyleSheet("font-size: 18px; color: white;")
        btn.clicked.connect(self.connexion)
        connexion_layout.addWidget(btn)
        btn = QPushButton("S'inscrire")
        btn.setStyleSheet("font-size: 18px; color: white;")
        btn.clicked.connect(self.activate_tab_inscription)
        connexion_layout.addWidget(btn)
        connexion = QWidget()
        connexion.setLayout(connexion_layout)
        self.stacklayout.addWidget(connexion)

        label = QLabel("Entrez vos identifiants et mot de passe pour créé votre compte : ")
        label.setStyleSheet("font-size: 18px; color: white;")
        inscription_layout.addWidget(label)
        self.user_id_inscription = QLineEdit()
        self.user_id_inscription.setPlaceholderText("Identifiant")
        self.user_id_inscription.setStyleSheet("font-size: 18px; color: white;")
        inscription_layout.addWidget(self.user_id_inscription)
        self.password_inscription = QLineEdit()
        self.password_inscription.setPlaceholderText("Mot de passe")
        self.password_inscription.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_inscription.setStyleSheet("font-size: 18px; color: white;")
        inscription_layout.addWidget(self.password_inscription)
        self.password_confirmation = QLineEdit()
        self.password_confirmation.setPlaceholderText("Confirmation de mot de passe")
        self.password_confirmation.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirmation.setStyleSheet("font-size: 18px; color: white;")
        inscription_layout.addWidget(self.password_confirmation)
        inscription = QWidget()
        inscription.setLayout(inscription_layout)
        self.stacklayout.addWidget(inscription)
        btn = QPushButton("Créer son compte")
        btn.clicked.connect(self.inscription)
        btn.setStyleSheet("font-size: 18px; color: white;")
        btn.pressed.connect(self.inscription)
        inscription_layout.addWidget(btn)

        self.catalog_db = Database("catalogue.csv")
        label = QLabel("Catalogue de nos produits")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        catalog_layout.addWidget(label)
        self.product_model = ProduitModel(self.catalog_db)
        self.table_catalog = QTableView()
        self.table_catalog.setModel(self.product_model)
        self.table_catalog.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        catalog_layout.addWidget(self.table_catalog)
        catalog = QWidget()
        catalog.setLayout(catalog_layout)
        self.stacklayout.addWidget(catalog)

        page = QWidget()
        page.setStyleSheet("background-color: #380059;")
        page.setLayout(page_layout)
        self.setCentralWidget(page)


    def activate_tab_inscription(self):
        self.stacklayout.setCurrentIndex(1)
        print("Transition vers la page d'inscription")
        return 0

    def activate_tab_catalog(self):
        self.stacklayout.setCurrentIndex(2)
        print("Transition vers catalog.")
        return 0

    def connexion(self):
        user_id = self.user_id_connexion.text()
        password = self.password_connexion.text()
        if(self.session.AUTH(user_id, password)):
            print("L'utilisateur est connecté.")
            self.activate_tab_catalog()
            return 0
        else :
            print("ERROR [2] : L'utilisateur n'a pas été authentifié.")
            return 2

    def inscription(self):
        user_id = self.user_id_inscription.text()
        password = self.password_inscription.text()
        confirmation = self.password_confirmation.text()
        if(password == confirmation):
            if(self.session.REGISTER(user_id, password)):
                print("Le compte utilisateur a été créé.")
            else :
                print("ERROR [1] : Le compte utilisateur n'a pas été créé.")
                return 1
        else:
            print("Les mots de passe ne correspondent pas.")
            return 1

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)
with open("styles.qss", "r", encoding="utf-8") as fichier:
    app.setStyleSheet(fichier.read())
window = MainWindow()
window.show()
app.exec()
=======
from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtGui import (
    QIcon,
)
from PyQt6.QtWidgets import (
    QApplication, QDialog,
)

import sys # Permet l'interaction avec le système d'exploitation

from src.utils.bootstrap import load_database
from src.utils.helpers import load_stylesheet
from src import config
from src.utils import utils_config

#=============================================================================#
# IMPORTATION DES FENÊTRES                                                    #
#=============================================================================#
from src.ui.source_dialog import SourceDialog
from src.ui.auth_window import AuthWindow
from src.ui.splash import SplashDialog

#=============================================================================#
# DEMARRAGE DE L'APPLICATION                                                  #
#=============================================================================#
def main() -> int:
    """Démarre et gère l'application dans sa globalité.

    Returns:
        int: Code de fermeture de l'application.
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(config.FAVICON_PATH)))
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
 
    # Demande le type de BDD à l'utilisateur
    dialog = SourceDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted.value:
        return 0  # Quitter l'app si l'utilisateur ferme la fenêtre sans choisir
 
    # Charger la base de données
    utils_config.CSV = dialog.is_csv()
    load_database()
 
    # Afficher la fenêtre de connexion
    window = AuthWindow()
    window.showMaximized()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
>>>>>>> d980c0ff9329379a40949afbf498f8913af0e7b5
