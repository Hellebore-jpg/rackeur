from __future__ import annotations 

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn
from ..utils.csv_utils import DB_Reader, Database
from .. import config

from .main_page import MainPage
from .add_product import AddProductPage

class GestionUserPage(Page):
    """Page principale affichée après la connexion.
    """

    def __init__(self, app_window) -> None:
        """Lance la page principale de l'application.
        """
        super().__init__()
        self.app_window = app_window
        self.setWindowTitle("users")
        self.setWindowTitle("users")
        self._details_ouvert = None
        self._panneaux = []
        self.database = Database("utilisateurs.csv")
        self.refresh()

    def refresh(self) -> None:
        """Reconstruit toute la grille à partir des données actuelles."""
        for panneau in self._panneaux:
            panneau.deleteLater()
        self._panneaux = []
        self._details_ouvert = None

        reader = DB_Reader(self.database)
        users = reader.READ()

        content = QWidget()
        layout = QVBoxLayout(content)
        liste = QVBoxLayout()

        for index, ligne in enumerate(users):
            row = QHBoxLayout()
            for valeur in ligne:
                row.addWidget(QLabel(str(valeur)))
            btn_delete = QPushButton("Supprimer")
            btn_delete.setProperty("class", "product-button")
            btn_delete.clicked.connect(lambda checked=False, i=index: self.delete_user(i))
            row.addWidget(btn_delete)
            liste.addLayout(row)

        layout.addLayout(liste)

        btn1: NavBtn = {"win_class": MainPage, "title": "main", "btn_title": "Catalogue"}
        btn2: NavBtn = {"win_class": AddProductPage, "title": "add_product", "btn_title": "Ajouter un produit"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="gestion_user", navbtns=[btn1, btn2]))
        

    def delete_user(self, index_product: int):
        self.database.DELETE(index_product)
        self.database.SAVE_FILE()
        self.refresh()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None