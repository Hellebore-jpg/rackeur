from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QListView,
)

from ..utils.helpers import make_header, make_background, make_card, RoundedImage
from .. import config

class SourceDialog(QDialog):
    """Fenêtre de séléction du type de base de données.
    """
    def __init__(self) -> None:
        """Crée la fenêtre de séléction du type de base de données.
        """
        super().__init__()
        self.setWindowTitle("Rackeur | Type de la base de données")
        self.setFixedSize(480, 600)
 
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
 
        title, subtitle = make_header("Type de données", "Choisissez le format de votre base de données")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(18)
 
        label = QLabel("Type")
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
 
        self.combo: QComboBox = QComboBox()
        self.combo.addItems(["CSV", "SQLite"])
        self.combo.setCursor(Qt.CursorShape.PointingHandCursor)
        view = QListView()
        self.combo.setView(view)
        popup = view.window()
        assert popup is not None
        popup.setWindowFlags(
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout.addWidget(self.combo)
        layout.addSpacing(22)
 
        self.continue_button: QPushButton = QPushButton("Continuer")
        self.continue_button.setObjectName("primaryButton")
        self.continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.continue_button.clicked.connect(self.accept)
        layout.addWidget(self.continue_button)
 
        root = make_background(make_card(content), RoundedImage(config.USER_PLACEHOLDER_PATH))
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)
 
    def is_csv(self) -> bool:
        return self.combo.currentText() == "CSV"