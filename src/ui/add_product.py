from __future__ import annotations 

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QLineEdit, QComboBox, QMessageBox,
    )
from PyQt6.QtGui import QIntValidator

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn
from ..utils import csv_utils, sqlite_utils, utils_config
from .. import config


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
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.refresh()

    def refresh(self) -> None:
        self._details_ouvert = None

        content = QWidget()
        layout = QVBoxLayout(content)

        bloc = QFrame()
        bloc.setProperty("class", "create-card")
        bloc.setFixedWidth(1600)
        bloc_layout = QVBoxLayout(bloc)
        bloc_layout.setContentsMargins(8, 4, 8, 4)
        bloc_layout.setSpacing(10)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Nom du produit")
        bloc_layout.addWidget(self.name)

        self.price = QLineEdit()
        self.price.setPlaceholderText("Prix du produit")
        self.price.setValidator(QIntValidator(0, 999999, self.price))
        bloc_layout.addWidget(self.price)

        self.stock = QLineEdit()
        self.stock.setPlaceholderText("Nombre en stock")
        self.stock.setValidator(QIntValidator(0, 999999, self.stock))
        bloc_layout.addWidget(self.stock)

        self.quality = QComboBox()
        self.quality.addItems(["Neuf", "Bon État", "Correcte"])
        bloc_layout.addWidget(self.quality)

        bloc_description = QFrame()
        bloc_description.setProperty("class", "create-card")
        bloc_description.setFixedHeight(300)
        bloc_description_layout = QVBoxLayout(bloc_description)
        self.description = QLineEdit()
        self.description.setPlaceholderText("Description du produit")
        bloc_description_layout.addWidget(self.description)
        bloc_layout.addWidget(bloc_description)

        save_btn = QPushButton("Enregistrer le produit")
        save_btn.clicked.connect(self.save_product)
        bloc_layout.addWidget(save_btn)
        
        layout.addWidget(bloc, alignment=Qt.AlignmentFlag.AlignCenter)

        btn1: NavBtn = {"title": "gestion_user", "btn_title": "Gérer les utilisateurs"}
        btn2: NavBtn = {"title": "main", "btn_title": "Catalogue"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="add_product", navbtns=[btn1, btn2]))


    def save_product(self):
        name: str = self.name.text()
        price: str = self.price.text()
        stock: str = self.stock.text()
        quality: str = self.quality.currentText()
        description: str = self.description.text()
        liste: list = [name, price, description, stock, quality]
        if(self.verif_form(liste)):
            return

        self.database.CREATE(liste)
        self.database.SAVE_FILE()
        self.clear_form()
        self.show_popup()

    def verif_form(self, liste: list):

        if any(not champ.strip() for champ in liste):
            popup = QMessageBox(self)
            popup.setObjectName("popupWarning")
            popup.setWindowTitle("Champs requis")
            popup.setText("Veuillez remplir tous les champs obligatoires.")
            popup.setIcon(QMessageBox.Icon.Warning)
            popup.setStandardButtons(QMessageBox.StandardButton.Ok)
            popup.exec()
            return True
        return False
        
    def delete_product(self, index_product: int):
        self.database.DELETE(index_product)
        self.database.SAVE_FILE()
        self.refresh()

    def show_popup(self):
        popup = QMessageBox(self)
        popup.setObjectName("popupConfirmation")
        popup.setWindowTitle("Confirmation")
        popup.setText("Le produit a bien été enregisté")

        btn_confirm = popup.addButton(
            "OK",
            QMessageBox.ButtonRole.AcceptRole
        )
        popup.exec()

        if popup.clickedButton() == btn_confirm:
            self.app_window.switch_to("main")

    def clear_form(self):
        self.name.clear()
        self.price.clear()
        self.stock.clear()
        self.description.clear()
        self.quality.setCurrentIndex(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None