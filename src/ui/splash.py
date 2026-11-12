from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, pyqtSignal
from PyQt6.QtGui import (
    QFont, QFontDatabase, QKeyEvent, QPixmap, QShowEvent,
)
from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QGraphicsOpacityEffect,
)

from ..utils.helpers import BackgroundWidget
from .. import config

class SplashDialog(QWidget):
    """Écran titre : fondu entrant, pause, fondu sortant (6s), passer en appuyant sur la touche Entrer.
    """

    FADE_MS: int = 500
    HOLD_MS: int = 3000
    finished = pyqtSignal()

    def __init__(self) -> None:
        """Initialise l'écran titre.
        """
        super().__init__()
        self.setWindowTitle("The Rackeur")
        self.setWindowState(Qt.WindowState.WindowMaximized)

        font_id = QFontDatabase.addApplicationFont(str(config.FONT_PATH))
        families = QFontDatabase.applicationFontFamilies(font_id) if font_id != -1 else []

        title = QLabel("The Rackeur")
        title.setObjectName("splashTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if families:
            title.setFont(QFont(families[0]))

        icon = QLabel()
        icon.setPixmap(
            QPixmap(str(config.ICON_PATH)).scaled(
                400, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.addWidget(title)
        content_layout.addWidget(icon)

        self._effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(content)
        self._effect.setOpacity(0.0)
        content.setGraphicsEffect(self._effect)

        root = BackgroundWidget(config.BACKGROUND_PATH)
        root_layout = QVBoxLayout(root)
        root_layout.addStretch()
        root_layout.addWidget(content, alignment=Qt.AlignmentFlag.AlignHCenter)
        root_layout.addStretch()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)

        fade_in = QPropertyAnimation(self._effect, b"opacity", self)
        fade_in.setDuration(self.FADE_MS)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)

        fade_out = QPropertyAnimation(self._effect, b"opacity", self)
        fade_out.setDuration(self.FADE_MS)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)

        self._anim: QSequentialAnimationGroup = QSequentialAnimationGroup(self)
        self._anim.addAnimation(fade_in)
        self._anim.addPause(self.HOLD_MS)
        self._anim.addAnimation(fade_out)
        self._anim.finished.connect(self.finished.emit)

    def showEvent(self, event: QShowEvent | None) -> None:
        """Affiche la fenêtre d'intro.

        Args:
            event (QShowEvent | None): Evénement avec lequel l'écran dooit se lancer.
        """
        super().showEvent(event)
        self.activateWindow()
        self.setFocus()
        self._anim.start()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """Permet d'interompre l'intro en appuyant sur "Entrée"

        Args:
            event (QKeyEvent | None): Evénement lié à la touche.
        """
        if event is not None and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._anim.stop()
            self.finished.emit()
            return
        super().keyPressEvent(event)