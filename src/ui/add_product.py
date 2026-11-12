from __future__ import annotations 

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QLineEdit, QLCDNumber,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn
from ..utils.csv_utils import DB_Reader, Database
from .. import config

from .gestion_user import GestionUserPage
from .main_page import MainPage

class AddProductPage(Page):
    """Page principale affichée après la connexion.
    """

    def __init__(self, app_window) -> None:
        """Lance la page principale de l'application.
        """
        super().__init__()
        self.app_window = app_window
        self.setWindowTitle("Produits")
        self.setWindowTitle("Produits")
        self._details_ouvert = None
        self._panneaux = []
        self.database = Database("catalogue.csv")


        self._details_ouvert = None

        reader = DB_Reader(self.database)
        produits = reader.READ()

        content = QWidget()
        layout = QVBoxLayout(content)

        bloc = QFrame()
        bloc.setProperty("class", "create-card")
        bloc.setFixedWidth(700)
        bloc_layout = QVBoxLayout(bloc)
        bloc_layout.setContentsMargins(8, 4, 8, 4)
        bloc_layout.setSpacing(10)

        name = QLineEdit()
        name.setPlaceholderText("Nom du produit")
        bloc_layout.addWidget(name)

        price = QLCDNumber()
        bloc_layout.addWidget(price)

        bloc_description = QFrame()
        bloc.setProperty("class", "create-card")
        bloc.setFixedWidth(300)
        bloc_description_layout = QVBoxLayout(bloc_description)
        description = QLineEdit()
        bloc_description_layout.addWidget(description)
        bloc_layout.addLayout(bloc_description_layout)

        layout.addWidget(bloc)

        btn1: NavBtn = {"win_class": GestionUserPage, "title": "gestion_user", "btn_title": "Gérer les utilisateurs"}
        btn2: NavBtn = {"win_class": MainPage, "title": "main", "btn_title": "Catalogue"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="add_product", navbtns=[btn1, btn2]))

    def delete_product(self, index_product: int):
        self.database.DELETE(index_product)
        self.database.SAVE_FILE()
        self.refresh()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None