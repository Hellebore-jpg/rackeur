from __future__ import annotations 

from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QFrame, QPushButton, QSizePolicy, QLineEdit, QComboBox, QMessageBox, QTextEdit,
    )
from PyQt6.QtGui import QIntValidator, QDoubleValidator

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
        self.setWindowTitle("Ajouter/Modifier un produit")
        self._details_ouvert = None
        self._panneaux = []
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.index_product = -1
        self.refresh()

    def refresh(self) -> None:
        if utils_config.CSV:
            reader = csv_utils.DB_Reader(self.database)
        else:
            reader = sqlite_utils.DB_Reader(self.database)

        index_product = self.index_product
        is_edit = self.index_product >= 0
        if is_edit:
            print("index :", self.index_product, "| BODY base :", len(self.database.BODY))
            self.product = reader.SELECT(index_product).READ()
            print(self.product)

        self._details_ouvert = None
        content = QWidget()
        layout = QVBoxLayout(content)

        bloc = QFrame()
        bloc.setProperty("class", "create-card")
        bloc.setMaximumWidth(1600)
        bloc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bloc_layout = QVBoxLayout(bloc)
        bloc_layout.setContentsMargins(8, 4, 8, 4)
        bloc_layout.setSpacing(10)


        self.name = QLineEdit()
        if is_edit:
            self.name.setText(self.product[0])
        else :
            self.name.setPlaceholderText("Nom du produit")
        bloc_layout.addWidget(self.name)

        self.price = QLineEdit()
        self.price.setValidator(QDoubleValidator(0, 999999, 2, self.price))
        if is_edit:
            self.price.setText(str(self.product[1]))
        else : 
            self.price.setPlaceholderText("Prix du produit")
        bloc_layout.addWidget(self.price)

        self.stock = QLineEdit()
        self.stock.setValidator(QIntValidator(0, 999999, self.stock))
        if is_edit:
            self.stock.setText(str(self.product[3]))
        else : 
            self.stock.setPlaceholderText("Nombre en stock")
        bloc_layout.addWidget(self.stock)

        self.quality = QComboBox()
        self.quality.addItems(["Neuf", "Bon État", "Correcte"])
        if is_edit:
            self.quality.setCurrentText(self.product[4])
        bloc_layout.addWidget(self.quality)

        bloc_description = QFrame()
        bloc_description.setProperty("class", "create-card")
        bloc_description.setMinimumHeight(150)
        bloc_description.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bloc_description_layout = QVBoxLayout(bloc_description)
        self.description = QTextEdit()
        self.description.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        if is_edit:
            self.description.setPlainText(self.product[2])
        else : 
            self.description.setPlaceholderText("Description du produit")
        bloc_description_layout.addWidget(self.description)
        bloc_layout.addWidget(bloc_description)

        save_btn = QPushButton("Enregistrer le produit")
        save_btn.setProperty("class", "product-button")
        if is_edit:
            save_btn.clicked.connect(self.edit_product)
        else :
            save_btn.clicked.connect(self.save_product)
        bloc_layout.addWidget(save_btn)
        
        layout.addWidget(bloc)

        btn1: NavBtn = {"title": "gestion_user", "btn_title": "Gérer les utilisateurs"}
        btn2: NavBtn = {"title": "main", "btn_title": "Catalogue"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="add_product", navbtns=[btn1, btn2]))


    def save_product(self):
        name: str = self.name.text()
        price: str = self.price.text()
        stock: str = self.stock.text()
        quality: str = self.quality.currentText()
        description: str = self.description.toPlainText()
        liste: list = [name, price, description, stock, quality]
        if(self.verif_form(liste)):
            return

        self.database.CREATE(liste)
        self.database.SAVE_FILE()
        self.clear_form()
        self.show_popup()

    def edit_product(self):
        name: str = self.name.text()
        price: str = self.price.text()
        stock: str = self.stock.text()
        quality: str = self.quality.currentText()
        description: str = self.description.toPlainText()
        liste: list = [name, price, description, stock, quality]
        if self.verif_form(liste):
            return
        for col, valeur in enumerate(liste):
            self.database.UPDATE(valeur, [self.index_product, col])
        self.database.SAVE_FILE()
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.clear_form()
        self.index_product = -1
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

    def set_product_index(self, index_product: int) -> None:
        self.index_product = index_product
        self.refresh()

    def verif_type_page(self, index_product:int):
        if index_product == -1:
            return True
        else:
            return False