from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtCore import Qt, QRectF, QEvent, pyqtSignal
from PyQt6.QtGui import (
    QColor, QPainter, QPainterPath, QPaintEvent, QPixmap, QResizeEvent, QStandardItem, QStandardItemModel,
)
from PyQt6.QtWidgets import (
    QFrame, QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox, QScrollArea, QSizePolicy,
)

from pathlib import Path # Gère les chemins de fichiers
from typing import TypedDict
import re

from .. import config


def load_stylesheet() -> str:
    """Charge la feuille de style PyQt. Les chemins relatifs des ressources référencées via url(...) sont convertis en chemins absolus à partir de BASE_DIR.

    Returns:
        str: Contenu de la feuille de style avec les chemins résolus.
    """
    stylesheet: str = config.STYLESHEET_PATH.read_text(encoding="utf-8")
    def resolve_path(match: re.Match[str]) -> str:
        """Convertit un chemin relatif de url(...) en chemin absolu.

        Args:
            match (re.Match[str]): Correspondance de l'expression régulière.

        Returns:
            str: Chemin url('{chemin_absolu}') avec des séparateurs POSIX, compatible avec les feuilles de style Qt.
        """
        path: str = match.group(1).strip("\"'")
        absolute_path: Path = (config.BASE_DIR / path).resolve()
        return f"url('{absolute_path.as_posix()}')"
    
    stylesheet = re.sub(
        r"url\((.*?)\)",
        resolve_path,
        stylesheet
    )
    
    return stylesheet


def make_card(content: QWidget) -> QFrame:
    """Crée un Widget dans une carte arondie avec une ombre.

    Args:
        content (QWidget): Widget à intégrer.

    Returns:
        QFrame: Carte avec widget intégré.
    """
    card = QFrame()
    card.setObjectName("card")
    card.setFixedWidth(config.CARD_WIDTH)
 
    layout = QVBoxLayout(card)
    layout.setContentsMargins(32, 32, 32, 32)
    layout.addWidget(content)
 
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(50)
    shadow.setOffset(0, 12)
    shadow.setColor(QColor(0, 0, 0, 160))
    card.setGraphicsEffect(shadow)
    return card

def make_big_card(content: QWidget) -> QFrame:
    """Crée un Widget dans une grande carte arondie avec une ombre.

    Args:
        content (QWidget): Widget à intégrer.

    Returns:
        QFrame: Carte avec widget intégré.
    """
    card = QFrame()
    card.setObjectName("card")
    card.setMaximumWidth(config.BIG_CARD_WIDTH)
    card.setMaximumHeight(config.BIG_CARD_HEIGHT)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
 
    layout = QVBoxLayout(card)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.addWidget(content)
 
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(50)
    shadow.setOffset(0, 12)
    shadow.setColor(QColor(0, 0, 0, 160))
    card.setGraphicsEffect(shadow)
    return card

class RoundedImage(QWidget):
    """Image carrée aux coins arrondis.
    """

    def __init__(self, image_path: Path, size: int = 120, radius: int = 24) -> None:
        super().__init__()
        self.setFixedSize(size, size)
        self._radius: int = radius
        self._pixmap: QPixmap = QPixmap(str(image_path))
        if not self._pixmap.isNull():
            self._pixmap = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

    def paintEvent(self, event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self._radius, self._radius)
        painter.setClipPath(path)
        if self._pixmap.isNull():
            painter.fillPath(path, QColor("#020202"))  # Noir si il n'y a pas d'image
        else:
            x = (self.width() - self._pixmap.width()) // 2
            y = (self.height() - self._pixmap.height()) // 2
            painter.drawPixmap(x, y, self._pixmap)
        painter.end()

class BackgroundWidget(QWidget):
    """Crée l'arrière plan, garde la couleur du QSS en fallback.
    """
    
    def __init__(self, image_path: Path) -> None:
        """Charge l'image d'arrière plan.

        Args:
            image_path (Path): Chemin vers l'image d'arrière plan.
        """
        super().__init__()
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._pixmap: QPixmap = QPixmap(str(image_path))
        self._scaled: QPixmap = QPixmap()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        super().resizeEvent(event)
        if not self._pixmap.isNull():
            self._scaled = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

    def paintEvent(self, event: QPaintEvent | None) -> None:
        super().paintEvent(event)
        if self._scaled.isNull():
            return
        painter = QPainter(self)
        x = (self.width() - self._scaled.width()) // 2
        y = (self.height() - self._scaled.height()) // 2
        painter.drawPixmap(x, y, self._scaled)
        painter.end()

def make_background(card: QFrame, header: QWidget | None = None, bg_path: Path = config.BACKGROUND_PATH) -> QWidget:
    """Crée le widget d'arrière plan avec une carte au centre.

    Args:
        card (QFrame): Carte à mettre au centre.
        bg_path (Path): Chemin de l'image d'arrière plan.

    Returns:
        QWidget: Widget d'arrière plan.
    """
    root = BackgroundWidget(bg_path)
    root.setObjectName("root")
 
    layout = QVBoxLayout(root)
    layout.addStretch()
    if header is not None:
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(20)
    layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
    layout.addStretch()
    return root

class NavBtn:
    title: str
    btn_title: str

def make_global_background(card: QFrame, app_window, img: QWidget | None = None, bg_path: Path = config.BACKGROUND_PATH, current_page: str | None = None, navbtns: list[NavBtn] = []) -> QWidget:
    """Crée le widget d'arrière plan avec une carte au centre.

    Args:
        card (QFrame): Carte à mettre au centre.
        bg_path (Path): Chemin de l'image d'arrière plan.

    Returns:
        QWidget: Widget d'arrière plan.
    """
    pseudo = config.SESSION.USER[0]
    root = BackgroundWidget(bg_path)
    root.setObjectName("root")
 
    global_layout = QVBoxLayout(root)
    global_layout.addStretch()

    header = QVBoxLayout()
    title_layout = QHBoxLayout()
    if img is not None:
        title_layout.addWidget(img, alignment=Qt.AlignmentFlag.AlignHCenter)
        title_layout.addSpacing(20)
    title = QLabel(f"Bienvenu cher {pseudo}")
    title.setProperty("class", "title")
    title_layout.addWidget(title)

    navbar_layout = QHBoxLayout()

    for e in navbtns:
        btn = QPushButton(e["btn_title"])
        btn.setProperty("class", "onglet-button")
        btn.clicked.connect(lambda checked=False, page_title=e["title"]: app_window.switch_to(page_title))
        navbar_layout.addWidget(btn)

    header.addLayout(title_layout)
    header.addLayout(navbar_layout)
    global_layout.addLayout(header)

    row = QHBoxLayout()
    row.addStretch()
    row.addWidget(card)
    row.addStretch()
    container = QWidget()
    container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    container.setLayout(row)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
    scroll.setWidget(container)

    global_layout.addWidget(scroll, 1)
    return root

def make_header(title: str, subtitle: str) -> tuple[QLabel, QLabel]:
    """Crée une entête.

    Args:
        title (str): title de l'entête.
        subtitle (str): Sous title de l'entête.

    Returns:
        tuple[QLabel, QLabel]: Entête.
    """
    title_label = QLabel(title)
    title_label.setObjectName("title")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setObjectName("subtitle")
    return title_label, subtitle_label

class Page(QWidget):
    """Base des pages : se comporte comme un QMainWindow avec setCentralWidget."""

    def __init__(self) -> None:
        super().__init__()
        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(0, 0, 0, 0)

    def setCentralWidget(self, widget: QWidget) -> None:
        while (item := self._root_layout.takeAt(0)) is not None:
            if item.widget() is not None:
                item.widget().deleteLater()
        self._root_layout.addWidget(widget)

class CheckableComboBox(QComboBox):
    """Menu déroulant avec des cases à cocher (sélection multiple)."""

    selectionChanged = pyqtSignal(list)  # émis à chaque changement, avec la liste des éléments cochés

    def __init__(self, options, selected=(), parent=None):
        super().__init__(parent)
        self._placeholder = "Permissions"

        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText(self._placeholder)
        self.setMaxVisibleItems(len(options))

        for option in options:
            item = QStandardItem(option)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(
                Qt.CheckState.Checked if option in selected else Qt.CheckState.Unchecked,
                Qt.ItemDataRole.CheckStateRole,
            )
            self.model().appendRow(item)

        self.setCurrentIndex(-1)

        # Les clics sur le champ texte et sur la liste sont gérés par eventFilter
        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self)

        self.model().dataChanged.connect(self._on_data_changed)
        self.update_text()

    def eventFilter(self, obj, event):
        # Clic sur le texte : ouvre ou ferme la liste
        if obj is self.lineEdit() and event.type() == QEvent.Type.MouseButtonRelease:
            if self.view().isVisible():
                self.hidePopup()
            else:
                self.showPopup()
            return True

        # Clic sur un élément de la liste : coche/décoche sans fermer la liste
        if obj is self.view().viewport() and event.type() == QEvent.Type.MouseButtonRelease:
            index = self.view().indexAt(event.position().toPoint())
            if index.isValid():
                self.toggle_item(index)
            return True  # empêche la fermeture automatique

        return super().eventFilter(obj, event)

    def toggle_item(self, index):
        item = self.model().itemFromIndex(index)
        if item is None:
            return
        item.setCheckState(
            Qt.CheckState.Unchecked
            if item.checkState() == Qt.CheckState.Checked
            else Qt.CheckState.Checked
        )

    def _on_data_changed(self, *args):
        self.update_text()
        self.selectionChanged.emit(self.selected_items())

    def update_text(self):
        # Texte vide si rien n'est coché : le placeholder s'affiche alors tout seul
        self.lineEdit().setText(", ".join(self.selected_items()))

    def selected_items(self) -> list[str]:
        return [
            self.model().item(i).text()
            for i in range(self.model().rowCount())
            if self.model().item(i).checkState() == Qt.CheckState.Checked
        ]