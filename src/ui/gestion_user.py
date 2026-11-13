from __future__ import annotations 

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QCheckBox, QComboBox, QMessageBox,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn, CheckableComboBox
from ..utils import csv_utils, sqlite_utils, utils_config
from .. import config
from ..utils.session_utils import PERMISSIONS

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
        if utils_config.CSV:
            self.user_database = csv_utils.Database("utilisateurs.csv")
        else:
            self.user_database = sqlite_utils.Database("utilisateurs.db")
        self.checkboxes = []
        self.user_widgets = []
        self.refresh()

    def refresh(self) -> None:
        self.user_widgets.clear()
        for panneau in self._panneaux:
            panneau.deleteLater()
        self._panneaux = []
        self._details_ouvert = None

        if utils_config.CSV:
            reader = csv_utils.DB_Reader(self.user_database)
        else:
            reader = sqlite_utils.DB_Reader(self.user_database)
        users = reader.BODY

        content = QWidget()
        layout = QVBoxLayout(content)
        liste = QVBoxLayout()

        liste = QGridLayout()
        liste.setHorizontalSpacing(15)
        liste.setVerticalSpacing(8)

        for colonne, nom in enumerate(self.user_database.HEAD):
            label = QLabel(nom.capitalize())
            label.setProperty("class", "table-header")
            liste.addWidget(label, 0, colonne)
        nb_colonnes = len(self.user_database.HEAD)
        label_suppr = QLabel("Supprimer")
        label_suppr.setProperty("class", "table-header")
        liste.addWidget(label_suppr, 0, nb_colonnes)

        self.user_widgets = []
        for position, (real_id, ligne) in enumerate(users):
            rang = position + 1  # la ligne 0 est l'en-tête
            widgets = {"id": real_id, "role": None, "perm": None, "delete": None}

            for colonne, valeur in enumerate(ligne):
                if colonne == 2:
                    role = QComboBox()
                    role.addItems(["editor", "visiteur", "admin"])
                    index_role = role.findText(str(valeur).strip())
                    if index_role >= 0:
                        role.setCurrentIndex(index_role)
                    widgets["role"] = role
                    liste.addWidget(role, rang, colonne)

                elif colonne == 3:
                    perm = CheckableComboBox(PERMISSIONS, bits_to_liste(valeur))
                    perm.setFixedWidth(150)
                    widgets["perm"] = perm
                    liste.addWidget(perm, rang, colonne)

                else:
                    liste.addWidget(QLabel(str(valeur)), rang, colonne)

            check_delete = QCheckBox()
            widgets["delete"] = check_delete
            liste.addWidget(check_delete, rang, nb_colonnes, Qt.AlignmentFlag.AlignCenter)

            self.user_widgets.append(widgets)

            liste.setRowStretch(len(users) + 1, 1)

        layout.addLayout(liste)

        valid_btn = QPushButton("Valider les modifications")
        valid_btn.setProperty("class", "product-button")
        valid_btn.clicked.connect(self.on_valid_clicked)
        layout.addWidget(valid_btn)

        btn2: NavBtn = {"title": "main", "btn_title": "Catalogue"}
        btn1: NavBtn = {"title": "add_product", "btn_title": "Ajouter un produit"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="gestion_user", navbtns=[btn1, btn2]))

    def on_valid_clicked(self) -> None:
        if self.show_popup():
            self.valid_user()

    def valid_user(self) -> None:
        to_delete = []
        for w in self.user_widgets:
            real_id = w["id"]
            if w["delete"].isChecked():
                to_delete.append(real_id)
                continue
            self.user_database.UPDATE(w["role"].currentText(), [real_id, 2])
            self.user_database.UPDATE(liste_to_bits(w["perm"].selected_items()), [real_id, 3])

        for real_id in sorted(to_delete, reverse=True):
            self.user_database.DELETE(real_id)

        self.user_database.SAVE_FILE()
        if utils_config.CSV:
            self.user_database = csv_utils.Database("utilisateurs.csv")
        else:
            self.user_database = sqlite_utils.Database("utilisateurs.db")
        self.refresh()

    def show_popup(self) -> bool:
        """Demande confirmation. Renvoie True si l'utilisateur accepte."""
        popup = QMessageBox(self)
        popup.setObjectName("popupConfirmation")
        popup.setWindowTitle("Confirmation")
        popup.setIcon(QMessageBox.Icon.Question)
        popup.setText("Les informations des utilisateurs vont être modifiées. Continuer ?")

        btn_confirm = popup.addButton("Confirmer", QMessageBox.ButtonRole.AcceptRole)
        popup.addButton("Annuler", QMessageBox.ButtonRole.RejectRole)
        popup.setDefaultButton(popup.buttons()[1])  # « Annuler » par défaut, plus sûr
        popup.exec()

        return popup.clickedButton() == btn_confirm

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None

def bits_to_liste(bits: str) -> list[str]:
        """'1010' -> ['CREATE', 'UPDATE']"""
        bits = str(bits).strip().zfill(len(PERMISSIONS))
        return [nom for nom, bit in zip(PERMISSIONS, bits) if bit == "1"]

def liste_to_bits(cochees: list[str]) -> str:
    """['CREATE', 'UPDATE'] -> '1010'"""
    return "".join("1" if nom in cochees else "0" for nom in PERMISSIONS)
