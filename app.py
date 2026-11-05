from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                            QPushButton, QWidget, QPushButton, 
                            QListWidget, QHBoxLayout, QVBoxLayout, 
                            QFrame, QLabel, QLineEdit, 
                            QMenu, QCheckBox, QComboBox,
                            QDateEdit, QDateTimeEdit, QStackedLayout,
                            QDial, QDoubleSpinBox, QFontComboBox,
                            QLabel, QLCDNumber, QLineEdit,
                            QMainWindow, QProgressBar, QPushButton,
                            QRadioButton, QSlider, QSpinBox,
                            QTimeEdit, QVBoxLayout, QWidget)
from PyQt6.QtCore import QSize, Qt, QRect, QPropertyAnimation
from PyQt6.QtGui import QAction, QColor, QPalette
import sys
from src import api_utils, csv_utils, session_utils
from src.session_utils import Session
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
        acceuil_layout = QVBoxLayout()

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
        self.id = QLineEdit()
        self.id.setPlaceholderText("Identifiant")
        self.id.setStyleSheet("font-size: 18px; color: white;")
        connexion_layout.addWidget(self.id)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("font-size: 18px; color: white;")
        connexion_layout.addWidget(self.password)

        connexion = QWidget()
        connexion.setLayout(connexion_layout)
        self.stacklayout.addWidget(connexion)

        btn = QPushButton("Se Connecter")
        btn.clicked.connect(self.connexion)
        btn.setStyleSheet("font-size: 18px; color: white;")
        btn.pressed.connect(self.connexion)
        connexion_layout.addWidget(btn)
        acceuil = QWidget()
        acceuil.setLayout(acceuil_layout)
        self.stacklayout.addWidget(acceuil)

        page = QWidget()
        page.setStyleSheet("background-color: #380059;")
        page.setLayout(page_layout)
        self.setCentralWidget(page)

    def activate_tab_acceuil(self):
        self.stacklayout.setCurrentIndex(1)
        print("Transition vers l'acceuil.")
        return 0

    def connexion(self):
        id = self.id.text()
        password = self.password.text()
        if(self.session.REGISTER(id, password)): # Il faudra séparer l'inscription de la connexion plus tard si on rajoute les commandes ou d'autres données d'utilisateur. - Math
            if(self.session.AUTH(id, password)):
                print("Le compte utilisateur a été créé et connecté.")
                self.activate_tab_acceuil()
                return 0
            else :
                print("ERROR [2] : L'utilisateur n'a pas été authentifié.")
                return 2
        else:
            if(self.session.AUTH(id, password)): # J'ai rajouté ça ici parce-que tu pouvais pas te connecter si ton compte existait déjà, libre à toi de le suprimmer - Math
                print("Le compte utilisateur existe et s'est connecté.")
                self.activate_tab_acceuil()
                return 0
            else :
                print("ERROR [1] : Le compte utilisateur n'a pas été créé.")
                return 1

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
