from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import (
    QColor, QPainter, QPainterPath, QPaintEvent, QPixmap, QResizeEvent,
)
from PyQt6.QtWidgets import (
    QFrame, QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget,
)

from ..config import *
import re

def load_stylesheet() -> str:
    """Charge la feuille de style PyQt. Les chemins relatifs des ressources référencées via url(...) sont convertis en chemins absolus à partir de BASE_DIR.

    Returns:
        str: Contenu de la feuille de style avec les chemins résolus.
    """
    stylesheet: str = STYLESHEET_PATH.read_text(encoding="utf-8")
    def resolve_path(match: re.Match[str]) -> str:
        """Convertit un chemin relatif de url(...) en chemin absolu.

        Args:
            match (re.Match[str]): Correspondance de l'expression régulière.

        Returns:
            str: Chemin url('{chemin_absolu}') avec des séparateurs POSIX, compatible avec les feuilles de style Qt.
        """
        path: str = match.group(1).strip("\"'")
        absolute_path: Path = (BASE_DIR / path).resolve()
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
    card.setFixedWidth(CARD_WIDTH)
 
    layout = QVBoxLayout(card)
    layout.setContentsMargins(32, 32, 32, 32)
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

def make_background(card: QFrame, header: QWidget | None = None, bg_path: Path = BACKGROUND_PATH) -> QWidget:
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
     
def make_header(title: str, subtitle: str) -> tuple[QLabel, QLabel]:
    """Crée une entête.

    Args:
        title (str): Titre de l'entête.
        subtitle (str): Sous titre de l'entête.

    Returns:
        tuple[QLabel, QLabel]: Entête.
    """
    title_label = QLabel(title)
    title_label.setObjectName("title")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setObjectName("subtitle")
    return title_label, subtitle_label