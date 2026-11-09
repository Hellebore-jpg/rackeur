from __future__ import annotations

from PyQt6.QtCore import Qt, QPropertyAnimation, QRectF, QSequentialAnimationGroup
from PyQt6.QtGui import (
    QColor, QFont, QFontDatabase, QIcon, QKeyEvent, QPainter, QPainterPath, QPaintEvent, QPixmap,
    QResizeEvent, QShowEvent,
)
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget, QListView,
    QGraphicsOpacityEffect,
)

from dataclasses import dataclass
from pathlib import Path
import sys

from src.utils.csv_utils import *
from src.utils.session_utils import *

#=============================================================================#
# CONFIGURATION MANUELLE DE L'APPLICATION                                     #
#=============================================================================#

# VALEURS PERSONALISÉES
CARD_WIDTH: int = 380

# CHEMINS DE FICHIERS
BASE_DIR: Path = Path(__file__).parent.parent
STYLESHEET_PATH: Path = BASE_DIR / "assets/style.qss"
FAVICON_PATH: Path = BASE_DIR / "assets/img/favicon.png"
ICON_PATH: Path = BASE_DIR / "assets/img/icon.png"
USER_PLACEHOLDER_PATH: Path = BASE_DIR / "assets/img/user.png"
BACKGROUND_PATH: Path = BASE_DIR / "assets/img/background.png"
BACKGROUND_HOLES_PATH: Path = BASE_DIR / "assets/img/holes_background.png"
FONT_PATH: Path = BASE_DIR / "assets/font/Kablammo/Kablammo-Regular-VariableFont_MORF.ttf"

#=============================================================================#
# CONFIGURATION AUTOMATIQUE                                                   #
#=============================================================================#

# GESTION DE LA BASE DE DONNÉE CSV
HEADERT: list[type] | None = None # Header de la base de données
CATALOGUE: Database | None = None # Base de données en CSV

# CONFIGURATION GLOBALE
SESSION: Session # Gestion utilisateurs