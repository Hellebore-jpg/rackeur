from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget
)

from ..utils.helpers import make_header, make_background, make_card, RoundedImage
from .. import config
        
class MainPage(QMainWindow):
    """Page principale affichée après la connexion.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rackeur | Catalogue")
        # Construire l'interface du tableau ici
        title, subtitle = make_header("Page principale", "Vous êtes connecté")
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setCentralWidget(make_background(make_card(content), RoundedImage(config.USER_PLACEHOLDER_PATH)))