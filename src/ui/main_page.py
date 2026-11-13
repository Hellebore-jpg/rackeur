from __future__ import annotations 
import math
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QLineEdit,
)

from ..utils.helpers import Page, make_global_background, make_big_card, RoundedImage, NavBtn
from ..utils import csv_utils, sqlite_utils, utils_config
from .. import config

PAGE_SIZE = 30
class MainPage(Page):
    """Page principale affichée après la connexion.
    """

    def __init__(self, app_window) -> None:
        """Lance la page principale de l'application.
        """
        super().__init__()
        self.app_window = app_window
        self.setWindowTitle("self.produits")
        self._details_ouvert = None
        self._panneaux = []
        self.page = 0
        self.search_text = ""
        if utils_config.CSV:
            self.database = csv_utils.Database("catalogue.csv")
        else:
            self.database = sqlite_utils.Database("catalogue.db")
        self.refresh()
    
    def refresh(self, body = None) -> None:
        """Reconstruit toute la grille à partir des données actuelles."""
        for panneau in self._panneaux:
            panneau.deleteLater()
        self._panneaux = []
        self._details_ouvert = None

        if body is None:
            if utils_config.CSV:
                reader = csv_utils.DB_Reader(self.database)
            else:
                reader = sqlite_utils.DB_Reader(self.database)
            self.produits = reader.READ()
        else :
            self.produits = body

        if self.produits and isinstance(self.produits[0], str):
            self.produits = [self.produits]

        total_pages = max(1, math.ceil(len(self.produits) / PAGE_SIZE))
        self.page = min(self.page, total_pages - 1)
        debut = self.page * PAGE_SIZE
        fin = debut + PAGE_SIZE

        content = QWidget()
        layout = QVBoxLayout(content)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un produit...")
        self.search_bar.setText(self.search_text)
        self.search_bar.textChanged.connect(self.search_products)
        layout.addWidget(self.search_bar)

        grille = QGridLayout()
        grille.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        grille.setSpacing(10)
        colonnes = 6

        for index, ligne in enumerate(self.produits[debut:fin], start=debut):
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

            if config.SESSION.CHECK_PERM('DELETE'):
                btn_delete = QPushButton("Supprimer le produit")
                btn_delete.setProperty("class", "product-button")
                btn_delete.clicked.connect(lambda checked=False, i=index: self.delete_product(i))
                bloc_layout.addWidget(btn_delete)

            if config.SESSION.CHECK_PERM('EDIT'):
                btn_edit = QPushButton("Modifier le produit")
                btn_edit.setProperty("class", "product-button")
                bloc_layout.addWidget(btn_edit)
                btn_edit.clicked.connect(lambda checked=False, i=index: self.edit_product(i))

            position = index - debut
            rang = position // colonnes
            colonne = position % colonnes
            grille.addWidget(bloc, rang, colonne, Qt.AlignmentFlag.AlignTop)

        grille.setRowStretch((len(self.produits[debut:fin]) // colonnes) + 1, 1)

        layout.addLayout(grille)
        if total_pages > 1:
            nav = QHBoxLayout()
            nav.addStretch()

            btn_prev = QPushButton("◀ Précédent")
            btn_prev.setProperty("class", "product-button")
            btn_prev.setEnabled(self.page > 0)
            btn_prev.clicked.connect(lambda: self.change_page(-1))
            nav.addWidget(btn_prev)

            nav.addWidget(QLabel(f"Page {self.page + 1} / {total_pages}"))

            btn_next = QPushButton("Suivant ▶")
            btn_next.setProperty("class", "product-button")
            btn_next.setEnabled(self.page < total_pages - 1)
            btn_next.clicked.connect(lambda: self.change_page(1))
            nav.addWidget(btn_next)

            nav.addStretch()
            layout.addLayout(nav)

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
        self.app_window.switch_to("add_product", index_product)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None

    def search_products(self, text: str):
        column = [
            0, 2,
        ]
        self.search_text = text
        self.page = 0    
        self.produits = self.database.READER().SEARCH(text, column).READ()
        self.refresh(self.produits)
        self.search_bar.setFocus()
        self.search_bar.end(False)

    def change_page(self, delta: int) -> None:
        self.page += delta
        self.refresh(self.produits)