from assets.utils.csv_utils import Catalogue, Catalogue_Reader, CREATE_CSV
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                            QPushButton, QWidget, QPushButton, 
                            QListWidget, QHBoxLayout, QVBoxLayout, 
                            QFrame, QLabel, QLineEdit, 
                            QMenu, QCheckBox, QComboBox,
                            QDateEdit, QDateTimeEdit, QStackedLayout,
                            QDial, QDoubleSpinBox, QFontComboBox,
                            QLabel, QLCDNumber, QLineEdit,
                            QMainWindow, QProgressBar, QPushButton,
                            QRadioButton, QSlider, QSpinBox,
                            QTimeEdit, QVBoxLayout, QWidget)
from PyQt6.QtCore import QSize, Qt, QRect, QPropertyAnimation
from PyQt6.QtGui import QAction, QColor, QPalette
import sys
from random import choice
from layout_colorwidget import Color

if __name__ == '__main__':
    header_type: list[type] = [str, str, int]
    CREATE_CSV(header=['test1', 'test2', 'test3'])
    catalogue = Catalogue()
    catalogue.SAVE_CSV()
    reader = Catalogue_Reader(catalogue)
    reader.PRINT_CSV()

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle("My App")
        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        connexion_layout = QVBoxLayout()
        acceuil_layout = QVBoxLayout()

        page_layout.addLayout(button_layout)
        page_layout.addLayout(self.stacklayout)

        connexion = QWidget()
        connexion.setLayout(connexion_layout)
        self.stacklayout.addWidget(connexion)

        btn = QPushButton("Se Connecter")
        btn.pressed.connect(self.activate_tab_acceuil)
        connexion_layout.addWidget(btn)
        acceuil = QWidget()
        acceuil.setLayout(acceuil_layout)
        self.stacklayout.addWidget(acceuil)

        container = QWidget()
        container.setLayout(page_layout)
        self.setCentralWidget(container)


    def activate_tab_connexion(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_acceuil(self):
        self.stacklayout.setCurrentIndex(1)


    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
