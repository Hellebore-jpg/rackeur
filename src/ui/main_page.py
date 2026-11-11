from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QWidget, QGridLayout, QFrame, QLabel, QHBoxLayout, QPushButton, QSizePolicy,
)

from ..utils.helpers import make_header, make_global_background, make_big_card, RoundedImage
from ..utils.csv_utils import DB_Reader, Database
from .. import config
        
class MainPage(QMainWindow):
    """Page principale affichée après la connexion.
    """

    def __init__(self) -> None:
        """Lance la page principale de l'application.
        """
        super().__init__()
        self.setWindowTitle("Rackeur | Catalogue")
        # Construire l'interface du tableau ici
        self.setWindowTitle("Produits")
        content = QWidget()
        layout = QVBoxLayout(content)
        grille = QGridLayout()  # CHANGÉ : plus de parent, c'est layout qui la gère
        grille.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        grille.setSpacing(10)
        colonnes = 6

        database = Database("catalogue.csv")
        reader = DB_Reader(database)
        produits = reader.READ()
        self._details_ouvert = None
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
            details_layout = QVBoxLayout(details)
            ordre = ["description", "price", "quality"]

            for nom_colonne in ordre:
                i = database.HEAD.index(nom_colonne)
                valeur = ligne[i]

                if nom_colonne == "price":
                    prix = str(valeur).rstrip("0").rstrip(".")
                    valeur = f"{prix} €"
                    info = QLabel(f"Prix : {valeur}")

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

            bouton = QPushButton("Voir les détails")
            bouton.setProperty("class", "product-button")
            bloc_layout.addWidget(bouton)

            def toggle_details(checked=False, d=details, b=bouton, bloc=bloc):
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

            bouton.clicked.connect(toggle_details)

            rang = index // colonnes
            colonne = index % colonnes
            # CHANGÉ : AlignTop pour que les cartes voisines ne s'étirent pas
            grille.addWidget(bloc, rang, colonne, Qt.AlignmentFlag.AlignTop)


        # AJOUTÉ : ligne vide extensible sous la grille, pour que tout reste collé en haut
        grille.setRowStretch((len(produits) // colonnes) + 1, 1)

        layout.addLayout(grille)

        self.setCentralWidget(make_global_background(make_big_card(content), RoundedImage(config.USER_PLACEHOLDER_PATH)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._details_ouvert is not None:
            self._details_ouvert[0].hide()
            self._details_ouvert[1].setText("Voir les détails")
            self._details_ouvert = None