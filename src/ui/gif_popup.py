from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout


class GifPopup(QDialog):
    """Popup sans bordure, au premier plan, qui joue un GIF une seule fois."""

    def __init__(self, gif_path: Path, position, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(False)  # bloque les clics pendant l'animation

        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        self.movie = QMovie(str(gif_path))
        self.label.setMovie(self.movie)

        # Taille de la fenêtre = taille du GIF
        self.movie.jumpToFrame(0)
        self.resize(self.movie.currentPixmap().size())
        self.move(position - self.rect().center())

        self.movie.frameChanged.connect(self._on_frame_changed)
        self.movie.finished.connect(self.accept)  # si le GIF est déjà "1 boucle"

    def _on_frame_changed(self, frame_number: int):
        # Dernière frame atteinte -> on laisse son délai s'écouler puis on ferme
        count = self.movie.frameCount()
        if count > 0 and frame_number >= count - 1:
            QTimer.singleShot(self.movie.nextFrameDelay(), self.accept)

    def showEvent(self, event):
        super().showEvent(event)
        self.movie.start()