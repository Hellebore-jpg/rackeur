from __future__ import annotations 

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QCheckBox, QComboBox, QListWidget, QAbstractItemView,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn, CheckableComboBox
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
        self._details_ouvert = None
        self._panneaux = []
        self.user_database = Database("utilisateurs.csv")
        self.checkboxes = []
        self.user_widgets = []
        self.refresh()

    def refresh(self) -> None:
        for panneau in self._panneaux:
            panneau.deleteLater()
        self._panneaux = []
        self._details_ouvert = None

        reader = DB_Reader(self.user_database)
        users = reader.READ()

        content = QWidget()
        layout = QVBoxLayout(content)
        liste = QVBoxLayout()

        for index, ligne in enumerate(users):
            row = QHBoxLayout()
            widgets = {"role": None, "perm": None, "delete": None}
            for colonne, valeur in enumerate(ligne):
                if colonne == 2:  
                    role = QComboBox()
                    role.addItems(["editor", "visiteur", "admin"])
                    role_actuel = str(valeur).strip()
                    index_role = role.findText(role_actuel)
                    if index_role >= 0:
                        role.setCurrentIndex(index_role)
                    row.addWidget(role)
                elif colonne == 3:  # colonne des permissions
                    options = ["CREATE", "READ", "UPDATE", "DELETE"]
                    selected = [x.strip() for x in str(valeur).split(",") if x.strip()]

                    perm = CheckableComboBox(options, selected)
                    perm.setFixedWidth(150)
                    row.addWidget(perm)
                else:
                    row.addWidget(QLabel(str(valeur)))

            check_delete = QCheckBox("Supprimer")
            check_delete.setProperty("class", "product-button")
            row.addWidget(check_delete)
            widgets["delete"] = check_delete

            liste.addLayout(row)
            self.user_widgets.append(widgets)


        self.checkboxes.append(check_delete)
        layout.addLayout(liste)

        valid_btn = QPushButton("Valider les modifications")
        valid_btn.clicked.connect(self.valid_user)

        btn1: NavBtn = {"title": "main", "btn_title": "Catalogue"}
        btn2: NavBtn = {"title": "add_product", "btn_title": "Ajouter un produit"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="gestion_user", navbtns=[btn1, btn2]))

    def valid_user(self):
        indices_to_delete = []
        for index, widgets in enumerate(self.user_widgets):
            role = widgets["role"].currentText() if widgets["role"] else None
            self.user_database.UPDATE(role, [index, 2])

            perm = (
                [item.text() for item in widgets["perm"].selectedItems()]
                if widgets["perm"]
                else []
            )
            self.user_database.UPDATE(",".join(perm), [index, 3])
            
            if widgets["delete"].isChecked():
                indices_to_delete.append(index)

        for index in reversed(indices_to_delete):
            self.user_database.DELETE(index)


        self.user_database.SAVE_FILE()
        self.user_database = Database("utilisateur.csv")
        self.refresh()

    def delete_user(self, index_product: int):
        self.user_database.DELETE(index_product)
        self.user_database.SAVE_FILE()
        self.user_database = Database("utilisateurs.csv")
        self.refresh()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None