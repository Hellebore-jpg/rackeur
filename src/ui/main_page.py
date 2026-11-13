from __future__ import annotations 

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn
from ..utils import csv_utils, sqlite_utils, utils_config
from .. import config

class MainPage(Page):
    """Page principale affichée après la connexion.
    """

    def __init__(self, app_window) -> None:
        """Lance la page principale de l'application.
        """
        super().__init__()
        self.app_window = app_window
        self.setWindowTitle("Produits")
        self._details_ouvert = None
        self._panneaux = []
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.refresh()
    
    def refresh(self) -> None:
        """Reconstruit toute la grille à partir des données actuelles."""
        for panneau in self._panneaux:
            panneau.deleteLater()
        self._panneaux = []
        self._details_ouvert = None

        
        if utils_config.CSV:
            reader = csv_utils.DB_Reader(self.database)
        else:
            reader = sqlite_utils.DB_Reader(self.database)
        produits = reader.READ()

        content = QWidget()
        layout = QVBoxLayout(content)
        grille = QGridLayout()
        grille.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        grille.setSpacing(10)
        colonnes = 6

        for index, ligne in enumerate(produits):
            bloc = QFrame()
            bloc.setProperty("class", "product-card")
            bloc.setFixedWidth(270)
            bloc.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
            bloc_layout = QVBoxLayout(bloc)
            bloc_layout.setContentsMargins(8, 4, 8, 4)
            bloc_layout.setSpacing(10)
            header = QHBoxLayout()

            name = QLabel(ligne[0])
            name.setProperty("class", "product-name")
            stock = QLabel(f"En stock : {ligne[3]}")
            stock.setProperty("class", "product-stock")

            header.addWidget(name)
            header.addStretch()
            header.addWidget(stock)

            bloc_layout.addLayout(header)
            details = QFrame(self)
            details.setProperty("class", "product-details")
            self._panneaux.append(details)
            details_layout = QVBoxLayout(details)
            ordre = ["description", "price", "quality"]

            for nom_colonne in ordre:
                i = self.database.HEAD.index(nom_colonne)
                valeur = ligne[i]

                if nom_colonne == "price":
                    nombre = float(valeur)
                    if nombre.is_integer():
                        prix = str(int(nombre))
                    else:
                        prix = f"{nombre:.2f}"
                    info = QLabel(f"Prix : {prix} €")

                elif nom_colonne == "description":
                    info = QLabel(str(valeur))

                elif nom_colonne == "quality":
                    info = QLabel(f"Qualité : {valeur}")

                info.setWordWrap(True)
                info.setSizePolicy(
                    QSizePolicy.Policy.Preferred,
                    QSizePolicy.Policy.Minimum
                )
                details_layout.addWidget(info)

            details.hide()

            btn = QPushButton("Voir les détails")
            btn.setProperty("class", "product-button")
            bloc_layout.addWidget(btn)

            def toggle_details(checked=False, d=details, b=btn, bloc=bloc):
                if d.isVisible():
                    d.hide()
                    b.setText("Voir les détails")
                    self._details_ouvert = None
                    return

                if self._details_ouvert is not None:
                    self._details_ouvert[0].hide()
                    self._details_ouvert[1].setText("Voir les détails")

                pos = bloc.mapTo(self, QPoint(0, bloc.height()))
                d.setFixedWidth(bloc.width())
                d.move(pos)
                d.adjustSize()
                d.show()
                d.raise_()
                b.setText("Masquer les détails")
                self._details_ouvert = (d, b)

            btn.clicked.connect(toggle_details)

            btn_delete = QPushButton("Supprimer le produit")
            btn_delete.setProperty("class", "product-button")
            bloc_layout.addWidget(btn_delete)

            btn_edit = QPushButton("Modifier le produit")
            btn_edit.setProperty("class", "product-button")
            bloc_layout.addWidget(btn_edit)

            btn_edit.clicked.connect(lambda checked=False, i=index: self.edit_product(i))
            btn_delete.clicked.connect(lambda checked=False, i=index: self.delete_product(i))

            rang = index // colonnes
            colonne = index % colonnes
            grille.addWidget(bloc, rang, colonne, Qt.AlignmentFlag.AlignTop)

        grille.setRowStretch((len(produits) // colonnes) + 1, 1)

        layout.addLayout(grille)

        btn1: NavBtn = {"title": "gestion_user", "btn_title": "Gérer les utilisateurs"}
        btn2: NavBtn = {"title": "add_product", "btn_title": "Ajouter un produit"}
        self.setCentralWidget(make_global_background(make_big_card(content), app_window=self.app_window, img=RoundedImage(config.USER_PLACEHOLDER_PATH), current_page="main", navbtns=[btn1, btn2]))

    def delete_product(self, index_product: int):
        self.database.DELETE(index_product)
        self.database.SAVE_FILE()
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.refresh()

    def edit_product(self, index_product: int):
        self.app_window.switch_to("add_product")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None